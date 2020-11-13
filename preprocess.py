import os
import pandas as pd


class CoronaPreprocess:

    _CONDITION = ["confirmed", "deaths", "recovered"]
    _DAILY_REPO_PATH = "csse_covid_19_daily_reports/"
    _TIME_REPO_PATH = "csse_covid_19_time_series/"

    def __init__(self, data_repo=os.getcwd() + "/data/COVID-19/csse_covid_19_data"):
        self.data_repo = data_repo
        self.daily_repo = data_repo + "/csse_covid_19_daily_reports/"
        self.time_repo = data_repo + "/csse_covid_19_time_series/"
        self.date = "11-09-2020"
        self.country = "Korea, South"
        self.time_confirmed_df = pd.DataFrame()
        self.time_deaths_df = pd.DataFrame()
        self.time_recovered_df = pd.DataFrame()
        self.day_df = pd.DataFrame()
        self.print_repo()

    def _total_prep(self, df):
        df_idx = ["Confirmed", "Deaths", "Recovered"]
        df = df[df_idx].rename(
            columns={
                "Confirmed": "확진자 수",
                "Deaths": "사망자 수",
                "Recovered": "완치자 수",
            }
        )
        df = df.sum().reset_index().rename(columns={"index": "구분", 0: "합계"})
        return df

    def _daily_prep(self, df, date):
        df_idx = ["Confirmed", "Deaths", "Recovered", "Country_Region"]
        df = df[df_idx].rename(
            columns={
                "Confirmed": "확진자 수",
                "Deaths": "사망자 수",
                "Recovered": "완치자 수",
                "Country_Region": "국가 구분",
            }
        )
        df = (
            df.groupby("국가 구분")
            .sum()
            .reset_index()
            .sort_values(by=["확진자 수"], ascending=False)
        )
        return df

    def _time_series_prep(self, df, condition):
        drop_idx = ["Province/State", "Country/Region", "Lat", "Long"]
        df = df.drop(columns=drop_idx)
        df = df.sum().reset_index().rename(columns={"index": "date", 0: condition})
        return df

    def _time_series_prep_by_country(
        self,
        df,
        country,
        condition,
    ):

        expected_idx = ["Province/State", "Country/Region", "Lat", "Long"]
        # Data transform
        df = df.loc[df["Country/Region"] == country]
        df = df.drop(columns=expected_idx)
        df = df.sum()
        df = df.reset_index().rename(columns={"index": "date", 0: condition})
        return df

    def _merge_df_by_conditions(self, conditions=_CONDITION):
        c_df = self.time_confirmed_df
        d_df = self.time_deaths_df
        r_df = self.time_recovered_df
        merged_df = self._time_series_prep(c_df, conditions[0])
        merged_df = merged_df.merge(self._time_series_prep(d_df, conditions[1]))
        merged_df = merged_df.merge(self._time_series_prep(r_df, conditions[2]))
        merged_df = merged_df.rename(
            columns={
                "date": "날짜",
                "confirmed": "확진자 수",
                "deaths": "사망자 수",
                "recovered": "완치자 수",
            }
        )
        return merged_df

    def _merge_df_by_cond_with_country(self, country, conditions=_CONDITION):
        c_df = self.time_confirmed_df
        d_df = self.time_deaths_df
        r_df = self.time_recovered_df
        merged_df = self._time_series_prep_by_country(c_df, country, conditions[0])
        merged_df = merged_df.merge(
            self._time_series_prep_by_country(d_df, country, conditions[1])
        )
        merged_df = merged_df.merge(
            self._time_series_prep_by_country(r_df, country, conditions[2])
        )
        merged_df = merged_df.rename(
            columns={
                "date": "날짜",
                "confirmed": "확진자 수",
                "deaths": "사망자 수",
                "recovered": "완치자 수",
            }
        )
        return merged_df

    def print_repo(self):
        print(f"[DAILY REPO]: {self.daily_repo}\n[TIME REPO]: {self.time_repo}")
        return self

    def get_condition(self):
        return self._CONDITION

    def set_data_repo(self, data_repo_path):
        self.data_repo = data_repo_path
        self.set_daily_repo(data_repo_path + "/csse_covid_19_daily_reports/")
        self.set_time_repo(data_repo_path + "/csse_covid_19_time_series/")
        self.print_repo()
        return self

    def set_daily_repo(self, daily_repo_path):
        self.daily_repo = daily_repo_path
        self.print_repo()
        return self

    def set_time_repo(self, time_repo_path):
        self.time_repo = time_repo_path
        self.print_repo()
        return self

    def set_date(self, date):
        self.date = date
        return self

    def set_country(self, country):
        self.country = country
        return self

    def load_daily_data(self):
        daily_data_path = self.daily_repo + self.date + ".csv"
        self.day_df = pd.read_csv(daily_data_path)
        print(f"[LOADED]: {daily_data_path}")
        return self

    def load_time_data(self, conditions=_CONDITION):
        time_confirmed_data = (
            self.time_repo + f"time_series_covid19_{conditions[0]}_global.csv"
        )
        time_deaths_data = (
            self.time_repo + f"time_series_covid19_{conditions[1]}_global.csv"
        )
        time_recovered_data = (
            self.time_repo + f"time_series_covid19_{conditions[2]}_global.csv"
        )
        self.time_confirmed_df = pd.read_csv(time_confirmed_data)
        self.time_deaths_df = pd.read_csv(time_deaths_data)
        self.time_recovered_df = pd.read_csv(time_recovered_data)
        print(f"[LOADED]: {time_confirmed_data}")
        print(f"[LOADED]: {time_deaths_data}")
        print(f"[LOADED]: {time_recovered_data}")
        return self

    def start_total_prep(self):
        df = self.day_df
        df = self._total_prep(df)
        return df

    def start_daily_prep(self):
        df = self.day_df
        date = self.date
        df = self._daily_prep(df, date)
        return df

    def start_time_prep(self):
        conditions = self._CONDITION
        df = self._merge_df_by_conditions(conditions)
        return df

    def start_time_prep_by_country(self):
        contitions = self._CONDITION
        country = self.country
        df = self._merge_df_by_cond_with_country(country, contitions)
        return df

    def start(self):
        day_df = self.start_daily_prep()
        # print(day_df.head)
        time_df = self.start_time_prep()
        # print(time_df.head)
        time_df_country = self.start_time_prep_by_country()
        # print(time_df_country.head)
        return day_df, time_df, time_df_country


# if __name__ == "__main__":
#     prep = CoronaPreprocess()
#     prep.set_country("Korea, South")
#     prep.set_date("11-10-2020")
#     df = prep.start_time_prep()
#     print(df)