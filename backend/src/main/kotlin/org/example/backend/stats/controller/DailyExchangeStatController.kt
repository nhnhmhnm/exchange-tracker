package org.example.backend.stats.controller

import org.example.backend.stats.service.DailyExchangeStatService
import org.springframework.web.bind.annotation.*
import java.time.LocalDate

@RestController
@RequestMapping("/api/v1/daily-exchange")
class DailyExchangeStatController(
    private val dailyExchangeStatService: DailyExchangeStatService
) {
    @PostMapping
    fun getStats(@RequestParam date: LocalDate) {
        dailyExchangeStatService.DailyStats(date)
    }
}
