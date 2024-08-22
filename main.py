import fnbot

# Importing configuration files
# fnbot.load_config_json("./pybot.json")
# fnbot.load_config_toml("./pybot.toml")
fnbot.load_config_toml("./pybot.toml")

# Create a new configuration file `config.toml` or `config.json`
# to replace `pybot.toml` or `pybot.json`
# fnbot.load_config_json("./config.json")
# fnbot.load_config_toml("./config.toml")


# Importing plugins
# fnbot.insert_plugin("debug", "./plugins")
# fnbot.insert_plugin(["debug", ], "./plugins")
# fnbot.insert_plugins_dir("./plugins",)
# containing _plugin as follows:
# fnbot.insert_the_plugin("_debug", "./plugins")
# fnbot.insert_the_plugin(["_debug", ], "./plugins")
fnbot.insert_plugins_dir("./plugins",)

# Create a new folder `plugin` to replace `plugins`
# fnbot.insert_plugins_dir("./plugin",)



if "__main__" == __name__:
    fnbot.run()


