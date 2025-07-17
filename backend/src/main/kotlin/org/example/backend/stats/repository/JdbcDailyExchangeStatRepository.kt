package org.example.backend.stats.repository

import org.example.backend.stats.dto.DailyExchangeStatResponse
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate
import org.springframework.stereotype.Repository
import java.time.LocalDate

@Repository
class JdbcDailyExchangeStatRepository(
    private val jdbcTemplate: NamedParameterJdbcTemplate
) : DailyExchangeStatRepository {
    override fun getStatByDate(date: LocalDate): DailyExchangeStatResponse? {
        val sql = """ 
             WITH sorted_rates AS (
                 SELECT
                     e.bank_id,
                     e.currency_id,
                     e.rate,
                     e.timestamp,
                     ROW_NUMBER() OVER (PARTITION BY e.bank_id, e.currency_id ORDER BY e.rate) AS rn,
                     COUNT(*) OVER (PARTITION BY e.bank_id, e.currency_id) AS cnt
                 FROM exchange_rates e
                 WHERE e.timestamp >= :start AND e.timestamp < :end
             ),
             median_rates AS (
                 SELECT *
                 FROM sorted_rates
                 WHERE rn = FLOOR(cnt / 2) + 1
             ),
             aggregated AS (
                 SELECT
                     bank_id,
                     currency_id,
                     MIN(rate) AS lowest_rate,
                     MAX(rate) AS highest_rate,
                     MIN(timestamp) AS start_time,
                     MAX(timestamp) AS end_time
                 FROM sorted_rates
                 GROUP BY bank_id, currency_id
             )
             SELECT
                 a.bank_id,
                 a.currency_id,
                 a.lowest_rate,
                 a.highest_rate,
                 m.rate AS median_rate,
                 a.start_time,
                 a.end_time
             FROM aggregated a
             JOIN median_rates m
               ON a.bank_id = m.bank_id AND a.currency_id = m.currency_id
        """.trimIndent()

        val params = mapOf(
            "start" to date.atStartOfDay(),
            "end" to date.plusDays(1).atStartOfDay()
        )

        return jdbcTemplate.query(sql, params) { rs, _ ->
            DailyExchangeStatResponse(
                bankId = rs.getLong("bank_id"),
                currencyId = rs.getLong("currency_id"),
                lowestRate = rs.getBigDecimal("lowest_rate"),
                medianRate = rs.getBigDecimal("median_rate"),
                highestRate = rs.getBigDecimal("highest_rate"),
                startTime = rs.getTimestamp("start_time").toLocalDateTime(),
                endTime = rs.getTimestamp("end_time").toLocalDateTime()
            )
        }.firstOrNull()
    }

    override fun saveStat(stats: DailyExchangeStatResponse) {
        val sql = """
            INSERT INTO daily_exchange_stats (
                bank_id, currency_id, lowest_rate, median_rate, highest_rate, start_time, end_time
            ) VALUES (
                :bankId, :currencyId, :lowestRate, :medianRate, :highestRate, :startTime, :endTime
            )
            ON DUPLICATE KEY UPDATE
                lowest_rate = VALUES(lowest_rate),
                median_rate = VALUES(median_rate),
                highest_rate = VALUES(highest_rate),
                start_time = VALUES(start_time),
                end_time = VALUES(end_time)
        """
        val params = mapOf(
            "bankId" to stats.bankId,
            "currencyId" to stats.currencyId,
            "lowestRate" to stats.lowestRate,
            "medianRate" to stats.medianRate,
            "highestRate" to stats.highestRate,
            "startTime" to stats.startTime,
            "endTime" to stats.endTime
        )
        jdbcTemplate.update(sql, params)
    }
}
