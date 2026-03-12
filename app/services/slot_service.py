from datetime import timedelta
from app.utils.time_utils import parse_time, format_time


class SlotService:

    @staticmethod
    def calculate_slots(start_time, end_time, period_duration, recess_duration):

        start = parse_time(start_time)
        end = parse_time(end_time)

        if end <= start:
            return {
                "success": False,
                "error": "Ending time must be after starting time"
            }

        period_minutes = int(period_duration)
        recess_minutes = int(recess_duration)

        total_minutes = (end - start).total_seconds() / 60

        num_periods = 0
        temp_time = start

        while True:
            period_end = temp_time + timedelta(minutes=period_minutes)
            if period_end > end:
                break

            num_periods += 1
            temp_time = period_end

        if num_periods < 2:
            return {
                "success": False,
                "error": "Time range too short"
            }

        periods_before_recess = num_periods // 2

        slots = []
        current_time = start
        period_counter = 1

        for i in range(periods_before_recess):

            period_start = current_time
            period_end = period_start + timedelta(minutes=period_minutes)

            slots.append({
                "name": f"Period {period_counter}",
                "start_time": format_time(period_start),
                "end_time": format_time(period_end),
                "type": "period"
            })

            current_time = period_end
            period_counter += 1

        recess_start = current_time
        recess_end = recess_start + timedelta(minutes=recess_minutes)

        slots.append({
            "name": "Recess",
            "start_time": format_time(recess_start),
            "end_time": format_time(recess_end),
            "type": "recess"
        })

        current_time = recess_end

        while period_counter <= num_periods:

            period_start = current_time
            period_end = period_start + timedelta(minutes=period_minutes)

            if period_end > end:
                break

            slots.append({
                "name": f"Period {period_counter}",
                "start_time": format_time(period_start),
                "end_time": format_time(period_end),
                "type": "period"
            })

            current_time = period_end
            period_counter += 1

        return {
            "success": True,
            "data": {
                "slots": slots,
                "statistics": {
                    "total_periods": num_periods,
                    "start_time": format_time(start),
                    "end_time": format_time(end),
                    "total_minutes": int(total_minutes)
                }
            }
        }