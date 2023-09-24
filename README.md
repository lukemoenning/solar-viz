## Introduction
Engie is a multinational company based out of France. One of their big focuses is on sustainable, environmental-friendly energy through solar panels. In the University of Iowa’s Hackathon, Engie posted a challenge to analyze their solar panel data through their api. 
 
Solar Viz is a data analysis project, where we extract Engie’s api to answer their key questions and look at key metrics. Solar Viz first examines the solar panels conversion factor, which measures how much of the power input into the solar panel is output at the end. We then dive further into other key metrics in our in-depth analytics, where we explore payback analysis/cost analysis, and look at what it means to replace Iowa City’s main power supplier with solar panels.


## Development
1. Clone the repo - [github.com/lukemoenning/solar-viz](https://github.com/lukemoenning/solar-viz)

2. Build a docker image 
```
docker build -t solarviz .
```

3. Spin up containers 
```
docker-compose up -d --build
```

4. Navigate to [localhost:8501](http://localhost:8501/)

5. Tear down containers 
```
docker-compose down
```


For any suggestions, problems, or questions reach out to [moenningluke@gmail.com](moenningluke@gmail.com)
