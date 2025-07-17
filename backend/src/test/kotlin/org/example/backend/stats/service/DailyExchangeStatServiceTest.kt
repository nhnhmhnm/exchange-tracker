package org.example.backend.stats.service

import io.kotest.core.spec.style.BehaviorSpec
import io.mockk.*
import org.example.backend.stats.dto.DailyExchangeStatResponse
import org.example.backend.stats.repository.DailyExchangeStatRepository
import java.math.BigDecimal
import java.time.LocalDate
import java.time.LocalDateTime

class DailyExchangeStatServiceTest : BehaviorSpec({
    lateinit var repository: DailyExchangeStatRepository
    lateinit var service: DailyExchangeStatService

    beforeTest {
        repository = mockk(relaxed = true)
        service = DailyExchangeStatService(repository)
    }

    given("해당 날짜의 환율 데이터가 존재할 때") {
        val date = LocalDate.of(2025, 7, 16)
        val stat = DailyExchangeStatResponse(
                bankId = 1,
                currencyId = 1,
                lowestRate = BigDecimal("931.10"),
                medianRate = BigDecimal("932.20"),
                highestRate = BigDecimal("933.30"),
                startTime = LocalDateTime.of(2025, 7, 14, 9, 0),
                endTime = LocalDateTime.of(2025, 7, 14, 18, 0)
        )

        every { repository.getStatByDate(date) } returns stat
        every { repository.saveStat(any()) } just Runs

        `when`("서비스가 실행되면") {
            service.findStats(date)

            then("계산된 통계 데이터를 저장해야 한다") {
                verify(exactly = 1) { repository.saveStat(any()) }
            }
        }
    }

    given("해당 날짜에 환율 데이터가 존재하지 않을 때") {
        val date = LocalDate.of(2025, 7, 15)

        every { repository.getStatByDate(date)} returns null

        `when`("서비스를 실행하면") {
            service.findStats(date)

            then("저장 로직이 호출되지 않아야 한다") {
                verify(exactly = 0) { repository.saveStat(any()) }
            }
        }
    }
})
