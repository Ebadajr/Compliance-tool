{
  "nodes": [
    {
      "parameters": {
        "url": "https://admin-service.thndr-internal.app/compliance-service/admin/account-forms/VMsGQAe1eabXWcI4DOTs6A7rMiB2",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "accept",
              "value": "application/json, text/plain, */*"
            },
            {
              "name": "accept-language",
              "value": "en-US,en;q=0.9"
            },
            {
              "name": "origin",
              "value": "https://usertool.thndr-internal.app"
            },
            {
              "name": "priority",
              "value": "u=1, i"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"macOS\""
            },
            {
              "name": "sec-fetch-dest",
              "value": "empty"
            },
            {
              "name": "sec-fetch-mode",
              "value": "cors"
            },
            {
              "name": "sec-fetch-site",
              "value": "same-site"
            },
            {
              "name": "user-agent",
              "value": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
            }
          ]
        },
        "options": {
          "redirect": {
            "redirect": {}
          }
        }
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.4,
      "position": [
        -464,
        -496
      ],
      "id": "9d14303f-85e9-4ca8-95ce-8aeb80bf01bf",
      "name": "Get user's info from usertool",
      "credentials": {
        "httpHeaderAuth": {
          "id": "xq1XrcgpiRzuf6Mg",
          "name": "N8N Admin Token"
        }
      }
    }
  ],
  "connections": {
    "Get user's info from usertool": {
      "main": [
        []
      ]
    }
  },
  "pinData": {},
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "377e81cba7c72894ebba73767f8a8b9853ef68bd9d1616df7e6106eb33232fb3"
  }
}