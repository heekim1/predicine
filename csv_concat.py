import os
import pandas as pd


class Measurement():
    """The instrument produces measurements for a set of biological samples 
    over multiple timepoints. The class reads all the CSV files in the given directory, 
    and produces a single output CSV file that concatenates all the data. 
    """
    def __init__(self, directory, method="outer", key="sample_id", skipna=True):
        self.directory = directory
        self.csv_files = self.__get_csv_files()
        self.df_list = self.__convert_csv2df()
        self.merged_df = self.__merge_all(method=method, key=key)
        self.summary_df = self.__summarize(skipna=skipna)

    def get_input_csv_files(self):
        """Return cvs files in the directory

        Returns list of csv files
        """
        return self.csv_files

    def get_concatenated_data(self):
        """Return outer-joined dataframe on sample_id 

        Return merged dataframe
        """
        return self.merged_df
    
    def get_summary_data(self):
        """Return the average value of all the samples present at each time point recorded

        Return summarized datafram
        """
        return self.summary_df
    
    def export_csv(self) -> None:
        """Export both concatenated_data and summary_data in csv file
        """
        self.merged_df.to_csv('concatenated_data.csv', index=False)
        self.summary_df.to_csv('summary_data.csv', index=False)

    def __get_csv_files(self) -> list:
        """Get csv file in input directory.

        Return: 
            List of csv files
        """
        csv_files = []

        for filename in sorted(os.listdir(self.directory), key=lambda x: x.split('.')[0][1:]):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.directory, filename)
                csv_files.append(filepath)

        return csv_files

    def __convert_csv2df(self) -> list:
        """Convert list of csv files to list of data frame and then
        rename measurement with time point.

        Arg:
            List of csv files

        Return: 
            List of data frames
        """
        dfs = []
        for csv_file in self.csv_files:
            basename = os.path.basename(csv_file)
            time_point = basename.split('.')[0]
            df = pd.read_csv(csv_file)
            df = df.rename(columns={'measurement':time_point})
            dfs.append(df)

        return dfs

    def __merge_all(self, method="outer", key="sample_id") -> pd.DataFrame:
        """Merge data frames using how="outer" (default) and on=["sample_id"]

        Args:
            List of data frames

        Return: 
            A mereged data frame
        """
        if len(self.df_list) == 0:
            raise Exception("df_list is empty")
        
        if len(self.df_list) < 2:
            return self.df_list[0]
        
        merged_df = self.df_list[0]
        for df in self.df_list[1:]:
            merged_df = pd.merge(merged_df, df, how=method, on=['sample_id'])

        return merged_df

    def __summarize(self, skipna=True) -> pd.DataFrame:
        """Get average for each time spot. If skipna=True, then NaN values are excluded 
        while calculating mean. If skipna=False, NaN values are replaced with 0.

        Args:
            A merged data frame

        Return:
            A series of average for each time spot
        """

        summary_series = self.merged_df.iloc[:,1:].mean() if skipna else self.merged_df.fillna(0).iloc[:,1:].mean()
        summary_df = summary_series.reset_index().rename(columns={'index':'time_point', 0:'average'})

        return summary_df


if __name__ == "__main__":

    directory = '/Users/heeshinkim/Downloads/example_instrument_data'
    m = Measurement(directory)
    print("input_csv_file", m.get_input_csv_files())
    print("concatenated df", m.get_concatenated_data())
    print("summary skip nan", m.get_summary_data())
    m.export_csv()

    m2 = Measurement(directory, method="inner", skipna=False)
    print("summary no_skip nan", m2.get_summary_data())

