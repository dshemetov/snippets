# Katie's Sed Tricks
# Remove all quotes
sed 's/"//g'

# Remove all white space
sed 's/\s\s*//g'

# Replace all close brackets with new lines
sed '/]/\n/g'

# Remove duplicates
sort -u file.txt

# Take two columns from a JSON file and delete newlines
jq '.epidata[] | [.data_source, .signal]' < meta.json | tr -d '\n'

# Print file differences side-by-side
diff -y file1.txt file2.txt