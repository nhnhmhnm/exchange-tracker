package org.example.backend.stats.domain

import java.math.BigDecimal
import java.time.LocalDateTime

data class DailyExchangeStat(
    val bankId: Long,
    val currencyId: Long,

    val lowestRate: BigDecimal,
    val medianRate: BigDecimal,
    val highestRate: BigDecimal,

    val startTime: LocalDateTime,
    val endTime: LocalDateTime
)
