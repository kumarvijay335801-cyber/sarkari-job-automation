- name: Save detected jobs
  run: |
    git config user.name "Sarkari Job Bot"
    git config user.email "actions@github.com"

    git add seen_jobs.json

    if git diff --cached --quiet; then
      echo "No changes to save"
      exit 0
    fi

    git commit -m "Update detected jobs"

    git pull --rebase origin main

    git push origin main
