// SubOver is a tool for discovering subdomain takeovers
package main

import (
    "bufio"
    "crypto/tls"
    "encoding/json"
    "flag"
    "fmt"
    "github.com/parnurzeal/gorequest"
    "io/ioutil"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

// Structure for each provider stored in providers.json file
type ProviderData struct {
    Name     string   `json:"name"`
    Cname    []string `json:"cname"`
    Response []string `json:"response"`
}

var Providers []ProviderData

var Targets []string

var (
    HostsList  string
    Threads    int
    All        bool
    Verbose    bool
    ForceHTTPS bool
    Timeout    int
    OutputFile string
)

func InitializeProviders() {
    raw, err := ioutil.ReadFile("./providers.json")
    if err != nil {
        fmt.Println(err.Error())
        os.Exit(1)
    }

    err = json.Unmarshal(raw, &Providers)
    if err != nil {
        fmt.Printf("%s", err)
        os.Exit(1)
    }
}

func ReadFile(file string) (lines []string, err error) {
    fileHandle, err := os.Open(file)
    if err != nil {
        return lines, err
    }

    defer fileHandle.Close()
    fileScanner := bufio.NewScanner(fileHandle)

    for fileScanner.Scan() {
        lines = append(lines, fileScanner.Text())
    }

    return lines, nil
}

func Get(url string, timeout int, https bool) (resp gorequest.Response, body string, errs []error) {
    if https == true {
        url = fmt.Sprintf("https://%s/", url)
    } else {
        url = fmt.Sprintf("http://%s/", url)
    }

    resp, body, errs = gorequest.New().TLSClientConfig(&tls.Config{InsecureSkipVerify: true}).
        Timeout(time.Duration(timeout)*time.Second).Get(url).
        Set("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0").
        End()

    return resp, body, errs
}

func ParseArguments() {
    flag.IntVar(&Threads, "t", 20, "Number of threads to use")
    flag.StringVar(&HostsList, "l", "", "List of hosts to check takeovers on")
    flag.BoolVar(&All, "a", false, "Check all hosts regardless of CNAME")
    flag.BoolVar(&Verbose, "v", false, "Show verbose output")
    flag.BoolVar(&ForceHTTPS, "https", false, "Force HTTPS connections (Default: http://)")
    flag.IntVar(&Timeout, "timeout", 10, "Seconds to wait before timeout")
    flag.StringVar(&OutputFile, "o", "", "File to write enumeration output to")

    flag.Parse()
}

func CNAMEExists(key string) bool {
    for _, provider := range Providers {
        for _, cname := range provider.Cname {
            if strings.Contains(key, cname) {
                return true
            }
        }
    }

    return false
}

func Checker(target string) {
    TargetCNAME, err := net.LookupCNAME(target)
    fmt.Printf("DEBUG: %s=>%s\n", target, TargetCNAME)
    if err != nil {
        return
    } else {
        if (All != true && CNAMEExists(TargetCNAME)) || (All == true) {
            _, body, errs := Get(target, 120, ForceHTTPS)
            if len(errs) <= 0 {
                for _, provider := range Providers {
                    for _, response := range provider.Response {
                        if strings.Contains(body, response) == true {

                            switch provider.Name {
                            case "cloudfront":
                                _, body2, _ := Get(target, 120, true)
                                if strings.Contains(body2, response) == true {
                                    fmt.Printf("\n[\033[31;1;4m%s\033[0m] Takeover Possible At : %s", provider.Name, target)
                                }

                            default:
                                fmt.Printf("\n[\033[31;1;4m%s\033[0m] Takeover Possible At : %s", provider.Name, target)
                            }

                            break
                        }
                    }
                }
            }
        }
    }
}

func main() {
    ParseArguments()

    fmt.Println("")
    fmt.Println("SubOver v.1.2              Nizamul Rana (@Ice3man)")
    fmt.Println("==================================================\n")

    if HostsList == "" {
        fmt.Printf("[!] No hosts list specified !")
        fmt.Printf("\nUse -h for usage options\n")
        os.Exit(1)
    }

    InitializeProviders()
    Hosts, err := ReadFile(HostsList)
    if err != nil {
        fmt.Printf("\nread: %s\n", err)
        os.Exit(1)
    }

    Targets = append(Targets, Hosts...)

    hosts := make(chan string, Threads)
    processGroup := new(sync.WaitGroup)
    processGroup.Add(Threads)

    for i := 0; i < Threads; i++ {
        go func() {
            for {
                host := <-hosts
                if host == "" {
                    break
                }

                Checker(host)
            }

            processGroup.Done()
        }()
    }

    for _, Host := range Targets {
        hosts <- Host
    }

    close(hosts)
    processGroup.Wait()

    fmt.Printf("\n[~] Enjoy your hunt !\n")
}
