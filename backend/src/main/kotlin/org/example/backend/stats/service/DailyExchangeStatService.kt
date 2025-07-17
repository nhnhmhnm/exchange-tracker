package org.example.backend.stats.service

import jakarta.transaction.Transactional
import org.example.backend.stats.repository.DailyExchangeStatRepository
import org.springframework.stereotype.Service
import java.time.LocalDate

@Service
class DailyExchangeStatService(
    private val dailyStatsRepository: DailyExchangeStatRepository
) {
    @Transactional
    fun getStat(date: LocalDate) {
        val stat = dailyStatsRepository.getStatByDate(date)

        if (stat != null) {
            dailyStatsRepository.saveStat(stat)
        }
    }
}
