package org.example.backend.controller

import org.example.backend.dto.DailyExchangeStatResponse
import org.example.backend.service.DailyExchangeStatService
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import java.time.LocalDate

@RestController
@RequestMapping("/api/v1/daily-exchange")
class DailyStatController(
    private val dailyExchangeStatService: DailyExchangeStatService
) {
    @GetMapping
    fun getStats(@RequestParam date: LocalDate): {
        return dailyExchangeStatService.getStatsByDate(date)
    }
}
