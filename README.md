## OpenAI Gym enviroment simulating apps deployed to a cloud environment

### Parameters

The environment has two parameters (set an environment variables):
* `CLOUDSIM_GATEWAY_HOST` which defaults to `cloudsimplus-gateway`
* `CLOUDSIM_GATEWAY_PORT` which defaults 25333

### Testing 

In the `manual_tests`directory you can find three test scripts:

* `test_connect.py` - connects to the gateway directory and tries to tries to 
  add/remove virtual machines
* `test_finish.py` - connects to the gateway directly and runs the simulation 
  scenario until its end
* `test_run_env.py` - a smoke test which connects to the gateway through the 
  Open AI Gym, performs 5 steps and stops

For testing it is usually a good idea to redirect the environment to a local
gateway server by:

`export CLOUDSIM_GATEWAY_HOST=localhost`

### Developing 

* `pip install -e .` will install the package in dev mode and all its
  dependencies

### Deploying

We are working on getting the package to public PyPI repos. In the meantime you
can install the package with:

```
pip install -e git+https://github.com/pkoperek/gym_cloudsimplus#egg=gym_cloudsimplus
```
