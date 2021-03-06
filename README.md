### dbt

A data build tool

#### installation

```bash
› pip install dbt
```

#### configuration
  To create your first dbt project, run:
  ```bash
  › dbt init [project]
  ```
  This will create a sample dbt_project.yml file in the [project] directory with everything you need to get started.

  Next, create a `profiles.yml` file in the `~/.dbt` directory. If this directory doesn't exist, you should create it. The
  `dbt_project.yml` file should be checked in to your models repository, so be sure that it does *not* contain any database
  credentials! Make sure that all of your private information is stored in the `~/.dbt/profiles.yml` configuration file.

##### example dbt_project.yml
```yml

# configure dbt file paths (relative to dbt_project.yml)

# the package config is _required_. If other packages import this package,
# the name given below is used to reference this package
package:
  name: 'package_name'
  version: '1.0'

source-paths: ["models"]   # paths with source code to compile
target-path: "target"      # path for compiled code
clean-targets: ["target"]  # directories removed by the clean task
test-paths: ["test"]       # where to store test results

# default paramaters that apply to _all_ models (unless overridden below)

model-defaults:
  enabled: true           # enable all models by default
  materialized: false     # If true, create tables. If false, create views

# custom configurations for each model. Unspecified models will use the model-defaults information above.

models:
  pardot:                 # assuming pardot is listed in the models/ directory
    enabled: true         # enable all pardot models except where overriden (same as default)
    pardot_emails:        # override the configs for the pardot_emails model
      enabled: true       # enable this specific model (false to disable)
      materialized: true  # create a table instead of a view

      # You can choose sort keys, a dist key, or both to improve query efficiency. By default, materialized
      # tables are created with no sort or dist keys.
      #
      sort: ['@timestamp', '@userid'] # optionally set one or more sort keys on the materialized table
      dist: '@userid'                 # optionally set a distribution key on the materialized table

    pardot_visitoractivity:
      materialized: false
      sort: ['@timestamp']  # this has no effect, as sort and dist keys only apply to materialized tables

# add dependencies. these will get pulled during the `dbt deps` process.

repositories:
  - "git@github.com:analyst-collective/analytics"

```

##### example ~/.dbt/profiles.yml
```yml
user:                         # you can have multiple profiles for different projects
  outputs:
    my-redshift:              # uniquely named, you can have different targets in a profile
      type: redshift          # only type supported
      host: localhost         # any IP or fqdn
      port: 5439
      user: my_user
      pass: password
      dbname: dev
      schema: my_model_schema # the schema to create models in (eg. analyst_collective)
  run-target: my-redshift     # which target to run sql against
```

#### use

`dbt deps` to pull most recent version of dependencies

`dbt test` to check this validity of your SQL model files (this runs against the DB)

`dbt compile` to generate runnable SQL from model files

`dbt run` to run model files on the current `run-target` database

`dbt clean` to clear compiled files

#### docker

an alternate means of using dbt is with the docker image jthandy/dbt. if you already have docker installed on your system, run with:
```docker run -v ${PWD}:/dbt -v ~/.dbt:/root/.dbt jthandy/dbt /bin/bash -c "[type your command here]"
this can be run from any dbt project directory. it relies on the same configuration setup outlined above.

on linux and osx hosts, running this can be streamlined by including the following function in your bash_profile:
```
function dbt() {
    docker run -v ${PWD}:/dbt -v ~/.dbt:/root/.dbt jthandy/dbt /bin/bash -c "dbt ${1}"
}
```

at that point, any dbt command (i.e. `dbt run`) into a command line will execute within the docker container.

#### troubleshooting

If you see an error that looks like
> Error: pg_config executable not found

while installing dbt, make sure that you have development versions of postgres installed

```bash
# linux
sudo apt-get install libpq-dev python-dev

# osx
brew install postgresql
```

#### contributing

From the root directory of this repository, run:
```bash
› python setup.py develop
```

to install a development version of `dbt`.

#### design principles

dbt that supports an [opinionated analytics workflow](https://github.com/analyst-collective/wiki/wiki/Building-a-Mature-Analytics-Workflow:-The-Analyst-Collective-Viewpoint). Currently, dbt supports data modeling workflow. Future versions of dbt will support workflow for testing.

##### modeling data with dbt
- A model is a table or view built either on top of raw data or other models. Models are not transient; they are materialized in the database.
- Models are composed of a single SQL `select` statement. Any valid SQL can be used. As such, models can provide functionality such as data cleansing, data transformation, etc.
- Model files should be saved with a `.sql` extension.
- Each model should be stored in its own `.sql` file. The file name will become the name of the table or view in the database.
- Other models should be referenced with the `ref` function. This function will resolve dependencies during the `compile` stage. The only tables referenced without this function should be source raw data tables.
- Models should be minimally coupled to the underlying schema to make them robust to changes therein. Examples of how to implement this practice: a) provide aliases when specifying table and field names in models that select directly from raw data, b) minimize the number of models that select directly from raw data.
