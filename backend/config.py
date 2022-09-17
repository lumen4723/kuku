import config_default
import os


class Config(config_default.Config):
    pass


dir_path = os.path.dirname(os.path.realpath(__file__))
custom_config_exists = os.path.exists(dir_path + "/config_custom.py")

salt  = 'eCkvD5gW8sqyxVCN24kzC7fEefteLEZDswSQ9wMFPjRPpXt2DRFLmwyQptvPMFFPShXN4UpCrQP6TRVjYWDcwvT6XRnwwRCrMUbaVPstMwbbEXDyWur4Gnc5'

if custom_config_exists:
    import config_custom

    Config = config_custom.Config
