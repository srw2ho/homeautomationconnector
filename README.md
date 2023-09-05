# srw2ho homeautomationconnector

### Installation from Repository (online)
```bash
pip install git+https://github.com/srw2ho/homeautomationconnector.git
```

### Bundle python and project into .exe
```bash
pyinstaller tcpdevice2ppmpconnector.spec --onefile --clean
```

### Configuration
The configuration file has to be stored as "%.../homeautomationconnector.toml":
```toml

### Usage
```python
python -m homeautomationconnector



### Usage

```

# Build Docker
    docker build  . -t homeautomationconnector
    
# Run Docker
        docker run  --user root --privileged --rm -i -t homeautomationconnector:0.0.0 /bin/sh
        docker run -v --user root ${PWD}/etc/appconfigs/.:/etc/appconfigs/.  --privileged -t -i --rm   homeautomationconnector:0.0.0 /bin/sh
        docker run -v --user root ${PWD}/etc/appconfigs/.:/etc/appconfigs/.  --device /dev/gpiomem:/dev/gpiomem -t -i --rm   homeautomationconnector:0.0.0 /bin/sh