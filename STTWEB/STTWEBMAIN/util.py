
def convert_date(date):
    new_date = date[0:4] + date[5:7] + date[8:10]
    return new_date


def convert_seconds(seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    return "%d:%02d:%02d" % (hour, minute, sec)


def sort_results_by_date(elem):
    return int(convert_date(elem[2]))


def sort_results_by_occurrences(elem):
    return elem[1]


def exclude_from_results(results, exclude):
    for exclusion in exclude:
        new_results = []
        for result in results:
            if exclusion not in result[0].lower():
                new_results.append(result)
        results = new_results
    return results


def mark_frequent_results(results):
    try:
        time = results[0][3]
        for result in results[1:]:
            if result[3] - time < 30:
                result.append('full')
            else:
                time = result[3]
    except IndexError:
        pass
    return results
