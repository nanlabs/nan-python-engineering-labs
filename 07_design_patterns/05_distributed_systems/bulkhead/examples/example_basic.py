from concurrent.futures import ThreadPoolExecutor


def critical_job() -> str:
    return 'critical-ok'


def non_critical_job() -> str:
    return 'non-critical-ok'


def main() -> None:
    with ThreadPoolExecutor(max_workers=1) as critical_pool, ThreadPoolExecutor(max_workers=1) as aux_pool:
        a = critical_pool.submit(critical_job)
        b = aux_pool.submit(non_critical_job)
    print(a.result(), b.result())


if __name__ == '__main__':
    main()
