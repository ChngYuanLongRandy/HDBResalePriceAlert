formatted_timestamp=$(date "+%d%b%Y %H:%M")
curl -X POST -H "Content-Type: application/json" -d "{\"formattedTimestamp\": \"$formatted_timestamp\"}" localhost:5000/testSendEmail