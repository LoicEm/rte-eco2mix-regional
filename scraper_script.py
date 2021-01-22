import arrow

from scraping import scraper

if __name__ == "__main__":
    ref_date = arrow.get()
    query = scraper.QueryEnergyProduction(ref_date, live_query=True)
    res = query.query_regional_production_live()

    parsed_res = list(scraper.parse_response(res))



