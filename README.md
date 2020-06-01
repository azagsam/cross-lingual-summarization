# How to shuffle lines (simple linux command)

shuf output/language-model-characters.txt > output/language-model-characters-shuffled.txt

# extract lines with sed

example: sed -n 2,4p my_lines.txt > extracted_lines.txt

sed -n 1,53875683p output/language-model-characters-shuffled.txt > output/language-model-characters-shuffled-train.txt
sed -n 53875684,56868776p output/language-model-characters-shuffled.txt > output/language-model-characters-shuffled-test.txt
sed -n 56868777,59861870p output/language-model-characters-shuffled.txt > output/language-model-characters-shuffled-valid.txt


