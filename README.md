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
        docker run  --privileged --rm -i -t homeautomationconnector:0.0.0 /bin/sh
        docker run -v  /etc/appconfigs/.:/etc/appconfigs/. -v /logs/.:/logs/.  --privileged -t -i --rm   homeautomationconnector:0.0.0 /bin/sh
     