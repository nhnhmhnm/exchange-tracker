package org.example.backend.domain

import java.math.BigDecimal
import java.time.LocalDateTime

data class DailyExchangeStat(
    val bank: String,
    val currency: String,
    val highestRate: BigDecimal,
    val lowestRate: BigDecimal,
    val medianRate: BigDecimal,
    val startTime: LocalDateTime,
    val endTime: LocalDateTime
)
