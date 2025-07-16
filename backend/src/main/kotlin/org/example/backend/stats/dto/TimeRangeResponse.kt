package org.example.backend.dto

import java.time.LocalDateTime

data class TimeRangeResponse(
    val startTime: LocalDateTime,
    val endTime: LocalDateTime
)
