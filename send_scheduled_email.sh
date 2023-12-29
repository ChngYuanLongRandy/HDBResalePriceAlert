formatted_timestamp=$(date "+%d%b%Y %H:%M")
api_key="apikey"

curl -X POST -H "Content-Type: application/json" -H "API-KEY: $api_key" -d "{\"formattedTimestamp\": \"$formatted_timestamp\"}" localhost:5000/testSendEmail