from spider import crawl
import spider.args as args

"""Example to test spiders"""


def main():
    options = args.get_arg_parser().parse_args()
    results = crawl.crawl_job(
        job="software engineer",
        location="canada",
        skills=["aws", "python", "java", "c++"],
        page=0,
        platforms=[options.provider],
    )
    print("results are ", results)


if __name__ == "__main__":
    main()
