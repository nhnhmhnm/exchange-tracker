package org.example.backend.stats.dto

import java.math.BigDecimal
import java.time.LocalDateTime

data class DailyExchangeStatResponse(
    val bankId: Long,
    val currencyId: Long,
    val lowestRate: BigDecimal,
    val medianRate: BigDecimal,
    val highestRate: BigDecimal,
    val startTime: LocalDateTime,
    val endTime: LocalDateTime
)
