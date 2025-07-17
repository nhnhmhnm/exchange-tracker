package org.example.backend.stats.repository

import org.example.backend.stats.dto.DailyExchangeStatResponse
import java.time.LocalDate

interface DailyExchangeStatRepository {
    fun getStatByDate(date: LocalDate): DailyExchangeStatResponse?

    fun saveStat(stats: DailyExchangeStatResponse)
}
