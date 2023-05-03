from utils.dataset import AirDelayDataset
import os

data_path = '../datasets/airline-delay-analysis/2019.csv'
new_dataset_path = '../datasets/app-dataset/'
random_seed = 129 + 1123 + 923

def sample(dataframe, period=('2009-01-01', '2019-01-01'),
                fraction=0.002, path='', seed=0):
    print('Load set...')
    base = dataframe.get_date_period(period[0], period[1])
    base_frame = base.dataframe()
    base = base.derive(base_frame.filter(base_frame['CANCELLED'] == 0))
    # base = base.derive(base_frame)
    print('Total sample: {}'.format(len(base)))
    
    print('Sample set...')
    dataset = base.random_sample(fraction, seed)
    print('Total dataset sample: {}'.format(len(dataset)))
    
    
    print('Save dataset...')
    dataset.save(path)
    
if __name__ == '__main__':
    
    data = AirDelayDataset(data_path)
    train_path = os.path.join(new_dataset_path, './full/train.csv')
    test_path = os.path.join(new_dataset_path, './full/test.csv')
    sample(data, ('2009-01-01', '2019-01-01'),
           0.002, train_path, random_seed)
    sample(data, ('2019-01-01', '2020-01-01'),
           0.005, test_path, random_seed)