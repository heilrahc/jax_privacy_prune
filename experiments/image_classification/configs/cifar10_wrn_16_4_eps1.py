# coding=utf-8
# Copyright 2022 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Training a WRN-16-4 on CIFAR-10 with (1.0, 1e-5)-DP."""

from jax_privacy.src.training.image_classification import config_base
from jax_privacy.src.training.image_classification import data
from ml_collections import config_dict as configdict


@config_base.wrap_get_config
def get_config(config):
  """Experiment config."""

  config.experiment_kwargs = configdict.ConfigDict(
      dict(
          config=dict(
              num_updates=875,
              optimizer=dict(
                  name='sgd',
                  lr=dict(
                      init_value=2.0,
                      decay_schedule_name=None,
                      decay_schedule_kwargs=None,
                      relative_schedule_kwargs=None,
                      # decay_schedule_name='cosine_decay_schedule',
                      # decay_schedule_kwargs=configdict.ConfigDict(
                      #     {
                      #         'init_value': 1.0,
                      #         'decay_steps': 1.0,
                      #         'alpha': 0.0,
                      #     },
                      #     convert_dict=False),
                      # relative_schedule_kwargs=['decay_steps'],
                      ),
                  kwargs=dict(),
              ),
              model=dict(
                  model_type='wideresnet',
                  model_kwargs=dict(
                      depth=16,
                      width=4,
                  ),
                  restore=dict(
                      path=None,
                      params_key=None,
                      network_state_key=None,
                      layer_to_reset=None,
                  ),
              ),
              pruning=dict(
                  pruning_rate=0.206,
                  pruning_method='synflow'
              ),
              training=dict(
                  batch_size=dict(
                      init_value=4096,
                      per_device_per_step=128,
                      scale_schedule=None,  # example: {'2000': 8, '4000': 16},
                  ),
                  weight_decay=0.0,  # L-2 regularization,
                  train_only_layer=None,
                  dp=dict(
                      target_delta=1e-5,
                      clipping_norm=1.0,  # float('inf') or None to deactivate
                      stop_training_at_epsilon=8.0,  # None,
                      rescale_to_unit_norm=True,
                      noise=dict(
                          std_relative=10.0,  # noise multiplier
                          ),
                      # Set the following flag to auto-tune one of:
                      # * 'batch_size'
                      # * 'std_relative'
                      # * 'stop_training_at_epsilon'
                      # * 'num_updates'
                      # Set to `None` to deactivate auto-tunning
                      auto_tune=None,  # 'num_updates',  # None,
                      ),
                  logging=dict(
                      grad_clipping=True,
                      grad_alignment=False,
                      snr_global=True,  # signal-to-noise ratio across layers
                      snr_per_layer=False,  # signal-to-noise ratio per layer
                  ),
              ),
              averaging=dict(
                  ema=dict(
                      coefficient=0.9999,
                      start_step=0,
                  ),
                  polyak=dict(
                      start_step=0,
                  ),
              ),
              data=dict(
                  dataset=data.get_dataset(
                      name='cifar10',
                      train_split='train_valid',  # 'train' or 'train_valid'
                      eval_split='test',  # 'valid' or 'test'
                  ),
                  random_flip=True,
                  random_crop=True,
                  augmult=16,  # implements arxiv.org/abs/2105.13343
                  ),
              evaluation=dict(
                  batch_size=100,
              ))))

  return config
