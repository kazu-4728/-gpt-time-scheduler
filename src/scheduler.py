from datetime import datetime, timedelta


def schedule_jobs(products, start_date, work_time):
    """Return an optimized schedule respecting process order and due dates.

    Parameters
    ----------
    products : list[dict]
        Product definitions with ``name``, ``processes`` and ``due`` keys.
    start_date : str
        Starting date (YYYY-MM-DD).
    work_time : int | float
        Available work hours per day.

    Returns
    -------
    dict
        Schedule grouped by date, e.g. ``{"schedule": [...]}"``.
    """

    # sort products by due date to prioritise urgent items
    ordered = sorted(products, key=lambda p: p["due"])

    current = datetime.strptime(start_date, "%Y-%m-%d").date()
    remaining_hours = work_time

    plan = {}

    for prod in ordered:
        due = datetime.strptime(prod["due"], "%Y-%m-%d").date()

        for idx, proc in enumerate(prod["processes"], start=1):
            time_left = float(proc)

            while time_left > 0:
                # initialise day container
                day_key = current.isoformat()
                if day_key not in plan:
                    plan[day_key] = []
                    remaining_hours = work_time

                if remaining_hours == 0:
                    current += timedelta(days=1)
                    continue

                allocation = min(remaining_hours, time_left)
                plan[day_key].append(f"{prod['name']} 工程{idx}: {allocation:.1f}h")

                remaining_hours -= allocation
                time_left -= allocation

                if time_left > 0:
                    current += timedelta(days=1)

            if current > due:
                raise ValueError(f"{prod['name']} の加工が期限({due})を超えました")

        # move to next day if nothing left for this product
        if remaining_hours == 0:
            current += timedelta(days=1)

    schedule = [{"date": day, "tasks": tasks} for day, tasks in sorted(plan.items())]

    return {"schedule": schedule}
