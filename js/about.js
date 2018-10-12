async function commits() {
	var commitsList = {evanCommits: 0,
	duneCommits: 0,
	dylanCommits: 0,
	garrettCommits: 0,
	jonathanCommits: 0,
	danaCommits: 0}

	var settings = {
	  "async": false,
	  "crossDomain": true,
	  "url": 'https://gitlab.com/api/v4/projects/8550216/repository/commits?per_page=500',
	  "method": "GET",
	  "headers": {
	    "PRIVATE-TOKEN": "1sCuAzhEJxwzdaw1w9uL"
	  }
	}

	await $.ajax(settings).done(function (response) {
	  response.forEach(function(commit) {
	  	switch(commit['committer_name']) {
	  		case "Evan Heintschel":
	  		case "eheintschel":
				  commitsList.evanCommits++;
				  break;
			  case "Dune Blum":
			  case "dune297":
				  commitsList.duneCommits++;
				  break;
			  case "Dana Vaziri":
			  case "danavaziri":
				  commitsList.danaCommits++;
				  break;
			  case "Dylan Bottoms":
			  case "dylanbott":
				  commitsList.dylanCommits++;
				  break;
			  case "Jonathan Ray": 
			  case "JonathanAllenRay":
				  commitsList.jonathanCommits++;
				  break;
			  case "Garrett Bishop": 
			  case "gbishop888":
				  commitsList.garrettCommits++;
				  break;
	  	}
	  })
	});
	return commitsList;
}

async function issues() {
	var issuesList = {evanIssues: 0,
	duneIssues: 0,
	dylanIssues: 0,
	garrettIssues: 0,
	jonathanIssues: 0,
	danaIssues: 0}

	var settings = {
	  "async": false,
	  "crossDomain": true,
	  "url": 'https://gitlab.com/api/v4/projects/8550216/issues?per_page=500',
	  "method": "GET",
	  "headers": {
	    "PRIVATE-TOKEN": "1sCuAzhEJxwzdaw1w9uL"
	  }
	}

	await $.ajax(settings).done(function (response) {
	  response.forEach(function(issue) {
		if (issue["state"] == "closed") {
			switch(issue['closed_by']['username']) {
				case "eheintschel":
					issuesList.evanIssues++;
					break;
				case "dune297":
					issuesList.duneIssues++;
					break;
				case "danavaziri":
					issuesList.danaIssues++;
					break;
				case "dylanbott":
					issuesList.dylanIssues++;
					break;
				case "JonathanAllenRay":
					issuesList.jonathanIssues++;
					break;
				case "gbishop888":
					issuesList.garretIssues++;
					break;
			}
		}
	  })
	});
	return issuesList;
}