package org.example.backend.stats.dto

import java.time.LocalDateTime

data class TimeRangeResponse(
    val startTime: LocalDateTime,
    val endTime: LocalDateTime
)
