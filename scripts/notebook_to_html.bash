#!/bin/bash

# NOTE: Ideally, we would want this hooks to be stored in a separate repository
# so that it can be shared across different projects. But in interest of time, I am
# keeping it in this repo for now.
#
# HOW TO USE?
# 1. Navigate to your .git folder inside your project directory
# 2. In the .git folder there will be a folder called hooks, navigate into that folder
# 3. Create a new file called pre-commit and either you can paste the following code
# 4. Or you can paste the following command:
#
# ```bash
# #!/bin/sh
# source $(pwd)/scripts/notebooks_to_html.bash
# ```
# 5. Save and exit and run `chmod +x pre-commit`

# identify new notebooks added to the repo and convert them to html

echo "Converting new notebooks to html"

# Filter out any new or modified notebooks
newFiles=$(git diff --name-only --cached --diff-filter=AM | grep -E '\.ipynb$')

while IFS= read -r file; do
	if [ -f "$file" ]; then
		fileName=$(basename "$file")
		echo "Converting $file to html"
		jupyter nbconvert --no-output --to html "$file" --output "reports/${fileName%.*}.html"
	fi
done <<<"$newFiles"
