from bulldog import Model, Version
import pandas as pd
import time

model = Model({
    'df': pd.DataFrame(pd.np.ones((100, 100)))
})


@model.data_modifier
def data_step(data, factor):
    df = data['df']
    df *= factor
    return data  # this will modify the data


@model.business_logic
@model.checkpoint
def action1(data, commit):
    data['df'] /= 8000  # this has no effect whatsoever, we are modifying a copy
    commit("data_step", 9)
    return data  # consequently this does nothing


@model.analysis
@model.parallelizable
def analysis(data, history):
    df = data['df']
    time.sleep(3)
    print('fast 1', list(history.keys())[-1].name, pd.np.mean(df.values))


@model.analysis
@model.parallelizable
def analysis2(data, history):
    df = data['df']
    time.sleep(3)
    print('fast 2', list(history.keys())[-1].name, pd.np.mean(df.values))


@model.analysis
def analysis3(data, history):
    df = data['df']
    time.sleep(3)
    print('slow', list(history.keys())[-1].name, pd.np.mean(df.values))


def main():
    model.dispatch('action1')
    model.commit('data_step')
    print(model.history.keys())
    model.revert_version(Version(name='action1', step=1))
    # or equivalently `model.rollback(2)`
    print(model.history.keys())


if __name__ == '__main__':
    main()