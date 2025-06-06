# core/plugin_loader.py

def load_plugins(stage):
    class DummyPlugin:
        __name__ = "DummyPlugin"
        @staticmethod
        def run(target):
            print(f"[DummyPlugin] Running on {target}")

    return [DummyPlugin()]
