package org.example.backend.stats.repository

import org.example.backend.stats.dto.DailyExchangeStatResponse
import java.time.LocalDate

interface DailyExchangeStatRepository {
    fun findStatsByDate(date: LocalDate): List<DailyExchangeStatResponse>

    fun saveStats(stats: List<DailyExchangeStatResponse>)
}
