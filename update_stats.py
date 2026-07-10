import urllib.request
import json
import re

# 1. Fetch LeetCode Statistics
url = "https://leetcode.com/graphql"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
query = {
    "query": """
    query userProblemsSolved($username: String!) {
      matchedUser(username: $username) {
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """,
    "variables": {
      "username": "divyansh2005"
    }
}

total_solved = 1055 # fallback default
try:
    data = json.dumps(query).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=leetcode_headers if 'leetcode_headers' in locals() else headers, method="POST")
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        stats = res['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum']
        for entry in stats:
            if entry['difficulty'] == 'All':
                total_solved = entry['count']
        print(f"Latest LeetCode Solved Count: {total_solved}")
        
        # 2. Read and Update README.md
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Update text badge count
        content = re.sub(
            r"<!-- LEETCODE_TOTAL_START -->.*?<!-- LEETCODE_TOTAL_END -->",
            f"<!-- LEETCODE_TOTAL_START -->{total_solved}<!-- LEETCODE_TOTAL_END -->",
            content
        )

        # Update Typing SVG URL dynamically with Cyber Cyan theme
        new_typing_svg = (
            f'<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Press+Start+2P'
            f'&weight=600&size=14&duration=3000&pause=1000&color=08fdd8&center=true&vCenter=true&repeat=true'
            f'&width=620&height=45&lines=Scanning+Core+Modules...;Access+Granted%3A+DivyanshAhuja08;'
            f'Peak+Rating%3A+1982+%5BKnight%5D;{total_solved}+Problems+Solved...;Initializing+Algorithmic+Engine..." '
            f'alt="Typing SVG" /></a>'
        )
        content = re.sub(
            r"<!-- TYPING_SVG_START -->.*?<!-- TYPING_SVG_END -->",
            f"<!-- TYPING_SVG_START -->\n{new_typing_svg}\n<!-- TYPING_SVG_END -->",
            content,
            flags=re.DOTALL
        )

        # Write updated content back to README.md
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("README.md updated successfully with latest LeetCode stats.")
        
except Exception as e:
    print(f"Error updating stats: {e}")
