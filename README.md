# R-AR Verificator
Resource-Activity Requirements Compliance Verification Approach is developed to evaluate...

## Set up:

- Clone the project:
```bash
git clone https://github.com/marisol-barrientos/r-ar-verificator.git
```

- Create conda environment based on environment.yml file
1. Change to project directory path: **r-ar-verificator** in terminal

2. Create conda environment **r-ar-verificator**:
```bash
conda env create -f environment.yml
```
3. After installing all dependencies successfully, activate the environment:
```bash
conda activate r-ar-verificator
```
4. After creating the environment and activating it, execute the following commands one after each other in the command line to install all spaCy and coreferee models:
```bash
python -m spacy download en_core_web_md
```
```bash
python3 -m coreferee install en
```

If you encounter any issues, please reach out to the authors for assistance and guidance. Your input is invaluable in improving our work.
