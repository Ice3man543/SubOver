# SubOver

Subover is a Hostile Subdomain Takeover tool originally written in python but rewritten from scratch in Golang. Since it's redesign, it has been aimed with speed and efficiency in mind. Till date, SubOver detects 36 services which is much more than any other tool out there. The tool uses Golang concurrency and hence is very fast. It can easily detect and report potential subdomain takeovers that exist. The list of potentially hijackable services is very comprehensive and it is what makes this tool so powerful.

## Installing

You need to have Golang installed on your machine. There are no additional requirements for this tool.

```sh
git clone https://github.com/Ice3man543/SubOver.git .
cd SubOver
go build subover.go
```

## Usage

` ./subover.py -l subdomains.txt`
- `-l` List of Subdomains 
- `-t` Number of concurrent threads. (Default 10)
- `-v` Show verbose output (Default False)
- `-https` Force HTTPS Connection (Default HTTP)
- `-timeout` Set custom timeout (Default 10)
- `-h` Show help message

## Currently Checked Services

- Github
- Heroku
- Unbounce
- Tumblr
- Shopify
- Instapage
- Desk
- Tictail
- Campaignmonitor
- Cargocollective
- Statuspage
- Amazonaws
- Cloudfront
- Bitbucket
- Squarespace
- Smartling
- Acquia
- Fastly
- Pantheon
- Zendesk
- Uservoice
- WPEngine
- Ghost
- Freshdesk
- Pingdom
- Tilda
- Wordpress
- Teamwork
- Helpjuice
- Helpscout
- Cargo
- Feedpress
- Freshdesk
- Surge
- Surveygizmo
- Mashery


Count : 36
  
## Screenshot
![tool_in_action](https://raw.githubusercontent.com/Ice3man543/SubOver/master/subover.png)

## FAQ
**Q:** What should my wordlist look like?

**A:** Your wordlist should include a list of subdomains you're checking and should look something like:
```
backend.example.com
something.someone.com
apo-setup.fxc.something.com
```

## Your tool sucks!

Yes, you're probably correct. Feel free to:

- Not use it.
- Show me how to do it better.

# TODO

- Add more services :-)
- Improve the tool (There are many things that can be done :-) )

### Development

Want to contribute? Great! 

You can add more services or recommend any changes to the existing ones. Any kind of help is appreciated.

License
----

BSD 2-Clause "Simplified" License


## Contact

Meet me on Twitter: [@Ice3man543](https://twitter.com/ice3man543)

### Changelog

#### [1.1.0] - 2018-03-16

- Rewritten from scratch in Golang 
- This time it's damn fast because of Go Concurrency.
- The console output looks better :-)

#### [1.0.0] - 2018-02-04

- Initial Release with 35 Services written in Python.
- Pretty Slow :-)

## Credits

- [subjack : Hostile Subdomain Takeover Tool Written In GO](https://github.com/haccer/subjack)
- [Subdomain Takeover Scanner by 0x94](https://github.com/antichown/subdomain-takeover)
- [Anshumanbh : tko-subs](https://github.com/anshumanbh/tko-subs)

