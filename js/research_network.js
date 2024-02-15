var baseurl = document.body.getAttribute('data-baseurl');

const dataNodes = [
    { 
        id: 1, 
        title: "Clinical", 
        group: 1, 
        url: baseurl + "/keywords/clinical"
    }, 
    { 
        id: 2, 
        title: "Imaging", 
        group: 2,
        url: baseurl + "/keywords/imaging"
    }, 
    { 
        id: 3, 
        title: "Algorithmic", 
        group: 3,
        url: baseurl + "/keywords/algorithmic"
    },

    // clinical
    { 
        id: 4, 
        title: "Fetal Imaging", 
        group: 1, 
        url: baseurl + "/keywords/clinical/fetal-imaging"
    },
    { 
        id: 5, 
        title: "Breast Cancer", 
        group: 1, 
        url: baseurl + "/keywords/clinical/breast-cancer" 
    },
    { 
        id: 6, 
        title: "Diabetes", 
        group: 1, 
        url: baseurl + "/keywords/clinical/diabetes" 
    },
    { 
        id: 7, 
        title: "Chron's Disease", 
        group: 1, 
        url: baseurl + "/keywords/clinical/chrons-disease" 
    },
    { 
        id: 8, 
        title: "Cardiac", 
        group: 1, 
        url: baseurl + "/keywords/clinical/cardiac" 
    },

    // imaging
    { 
        id: 9, 
        title: "Qualitative MRI", 
        group: 2, 
        url: baseurl + "/keywords/imaging/qualitative-mri" 
    },
    { 
        id: 10, 
        title: "Radiological Reports", 
        group: 2, 
        url: baseurl + "/keywords/imaging/radiological-reports"  
    },
    { 
        id: 11, 
        title: "T1/T2 Mapping", 
        group: 2, 
        url: baseurl + "/keywords/imaging/t1-t2-mapping"  
    },
    { 
        id: 12, 
        title: "DWI", 
        group: 2, 
        url: baseurl + "/keywords/imaging/dwi" 
    },
    { 
        id: 13, 
        title: "Anatomical Imaging",
        group: 2, 
        url: baseurl + "/keywords/imaging/anatomical-imaging" 
    },
    { 
        id: 14, 
        title: "Ultrasound", 
        group: 2, 
        url: baseurl + "/keywords/imaging/ultrasound" 
    },
    { 
        id: 15, 
        title: "MRI", 
        group: 2, 
        url: baseurl + "/keywords/imaging/mri" 
    },
    { 
        id: 16, 
        title: "PET/CT", 
        group: 2, 
        url: baseurl + "/keywords/imaging/pet-ct" 
    },
    { 
        id: 17, 
        title: "Whole Slide Imaging", 
        group: 2, 
        url: baseurl + "/keywords/imaging/whole-slide-imaging" 
    },

    // algorithmic
    { 
        id: 18, 
        title: "NLP", 
        group: 3, 
        url: baseurl + "/keywords/algorithmic/nlp" 
    },
    { 
        id: 19, 
        title: "Relaxation Model Fitting", 
        group: 3, 
        url: baseurl + "/keywords/algorithmic/relaxation-model-fitting" 
    },
    { 
        id: 20, 
        title: "Segmentation", 
        group: 3, 
        url: baseurl + "/keywords/algorithmic/segmentation" 
    },
    { 
        id: 21, 
        title: "Registration", 
        group: 3, 
        url: baseurl + "/keywords/algorithmic/registration" 
    },
    { 
        id: 22, 
        title: "Image Reconstruction", 
        group: 3, 
        url: baseurl + "/keywords/algorithmic/image-reconstruction" 
    },
    { 
        id: 23, 
        title: "Visualization", 
        group: 3, 
        url: baseurl + "/keywords/algorithmic/visualization" 
    },
    { 
        id: 24, 
        title: "Super Resolution", 
        group: 3, 
        url: baseurl + "/keywords/algorithmic/super-resolution" 
    }
];

const dataLinksCategories = [
    { source: 1, target: 2 },
    { source: 2, target: 3 },
    { source: 3, target: 1 },

    { source: 1, target: 4 },
    { source: 1, target: 5 },
    { source: 1, target: 6 },
    { source: 1, target: 7 },
    { source: 1, target: 8 },

    { source: 2, target: 9 },
    { source: 2, target: 10 },
    { source: 2, target: 11 },
    { source: 2, target: 12 },
    { source: 2, target: 13 },
    { source: 2, target: 14 },
    { source: 2, target: 15 },
    { source: 2, target: 16 },
    { source: 2, target: 17 },

    { source: 3, target: 18 },
    { source: 3, target: 19 },
    { source: 3, target: 20 },
    { source: 3, target: 21 },
    { source: 3, target: 22 },
    { source: 3, target: 23 },
    { source: 3, target: 24 },
];

const dataLinksPapers = [
    { source: 6, target: 9 },
    { source: 6, target: 14 },
   
    { source: 13, target: 19 },
    { source: 19, target: 21 },
    { source: 21, target: 22 },
    { source: 22, target: 12 },
    { source: 12, target: 4 },
    { source: 4, target: 13 },

    { source: 20, target: 21 },
    { source: 21, target: 16 },

];


let width = window.innerWidth;
let height = window.innerHeight;

let nodeRadiusCenter = width / 50;
let nodeRadius = width / 100;
let linkDistanceCenter = width;
let linkDistance = width / 7.5;

let paddingCenter = 40;
let padding = 25;

let forceExternal = 300;
let forceStrength = 1;


// initialize svg using the svg in the html with ID = "research-network"
var svg = d3.select("#research-network")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;");

// Specify the color scale.
const color = d3.scaleOrdinal(d3.schemeCategory10);

// nodes
const node = svg.append("g")
    .selectAll()
    .data(dataNodes)
    .enter()
    .append("circle")
    .attr('class', 'nodeStyle')
    .attr("r", d => (d.id === 1 || d.id === 2 || d.id === 3) ? nodeRadiusCenter : nodeRadius)
    .attr("fill", d => color(d.group))
    .on("mouseenter", mouseEnter)
    .on("mouseleave", mouseLeave)
    .on("click", onClick);
        // window.location.href = d.url;

// lines for categories + topics
const linkCategories = svg.append("g")
    .selectAll()
    .data(dataLinksCategories)
    .enter()
    .append("line")
    .attr('class', 'link-categories');

// lines for the connections between the topics
dataLinksPapers.forEach(link => {
    link.source = dataNodes[link.source];
    link.target = dataNodes[link.target];
});

const linkPapers = svg.append("g")
    .selectAll()
    .data(dataLinksPapers)
    .enter()
    .append("line")
    .attr('class', 'link-papers');

// link force for the connections between the articles
const linkForce = d3.forceLink(dataLinksCategories)
    .id(d => d.id)
    .distance(link => {
        // Check if the link is between nodes 1-3
        if ((link.source.id === 1 || link.source.id === 2 || link.source.id === 3) &&
            (link.target.id === 1 || link.target.id === 2 || link.target.id === 3)) {
            return linkDistanceCenter;
        } else {
            return linkDistance;
        }
    });

    
const collideForce = d3.forceCollide(d => (d.id === 1 || d.id === 2 || d.id === 3) ? nodeRadiusCenter + paddingCenter : nodeRadius + padding);

// Create a simulation with several forces.
const simulation = d3.forceSimulation(dataNodes)
    .force("link", linkForce)
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collide", collideForce) // Add the forceCollide
    .force("radial", d3.forceRadial(d => {
        return d.id !== 1 && d.id !== 2 && d.id !== 3 ? forceExternal : 0; // Push nodes away if they are not in groups 1-3
    }, width / 2, height / 2).strength(forceStrength)) // Adjust the strength and radius as needed
    .on("tick", ticked);


    
const labelsCategories = svg.append("g")
    .attr("class", "node-center-text prevent-selection")
    .selectAll("text")
    .data(dataNodes.filter(d => d.id === 1 || d.id === 2 || d.id === 3))
    .enter().append("text")
    .text(d => d.title)
    .attr("dy", ".35em") // Vertically align text. Adjust as needed
    .attr("x", 0)
    .attr("y", 0)
    .on("mouseenter", mouseEnter)
    .on("mouseleave", mouseLeave)
    .on("click", onClick);

const labelsGroup1 = svg.append("g")
    .attr("class", "node-side-text prevent-selection")
    .selectAll("text")
    .data(dataNodes.filter(d => d.group === 1))
    .enter().append("text")
    .text(d => d.title)
    .attr("visibility", "hidden")
    .attr("dy", ".35em") // Vertically align text. Adjust as needed
    .attr("x", 0)
    .attr("y", 0)
    .on("mouseenter", mouseEnter)
    .on("mouseleave", mouseLeave)
    .on("click", onClick);

const labelsGroup2 = svg.append("g")
    .attr("class", "node-side-text prevent-selection")
    .selectAll("text")
    .data(dataNodes.filter(d => d.group === 2))
    .enter().append("text")
    .text(d => d.title)
    .attr("visibility", "hidden")
    .attr("dy", ".35em") // Vertically align text. Adjust as needed
    .attr("x", 0)
    .attr("y", 0)
    .on("mouseenter", mouseEnter)
    .on("mouseleave", mouseLeave)
    .on("click", onClick);

const labelsGroup3 = svg.append("g")
    .attr("class", "node-side-text prevent-selection")
    .selectAll("text")
    .data(dataNodes.filter(d => d.group === 3))
    .enter().append("text")
    .text(d => d.title)
    .attr("visibility", "hidden")
    .attr("dy", ".35em") // Vertically align text. Adjust as needed
    .attr("x", 0)
    .attr("y", 0)
    .on("mouseenter", mouseEnter)
    .on("mouseleave", mouseLeave)
    .on("click", onClick);

// Function to apply a small perturbation to node positions
function animateGraph() {
    let amplitude = .1; // Amplitude of the oscillation

    // Calculate new center coordinates, for example, a gentle oscillation
    const newCenterX = width / 2 + Math.sin(Date.now() / 1000) * amplitude; // 20 is the amplitude
    const newCenterY = height / 2 + Math.cos(Date.now() / 1000) * amplitude; // Oscillate in both X and Y

    // Update the center force
    simulation.force("center", d3.forceCenter(newCenterX, newCenterY));
    simulation.alpha(0.1).restart(); // Restart the simulation with a small alpha

}

// Start the animation with an interval
d3.interval(animateGraph, 50);

function onClick(event, d) {
    window.location.href = d.url;
}

function mouseEnter(event, d) {
    const enlargedRadius = (d.id === 1 || d.id === 2 || d.id === 3) ? nodeRadiusCenter * 2 : nodeRadius * 2;

    d3.select(this)
      .transition()
      .duration(150)
      .attr("r", enlargedRadius)  // Enlarge radius on hover

    labelsCategories.attr("visibility", "hidden");
    if (d.id === 1) {
        labelsGroup1.attr("visibility", "visible");
    } else if (d.id === 2) {
        labelsGroup2.attr("visibility", "visible");
    } else if (d.id === 3) {
        labelsGroup3.attr("visibility", "visible");
    } else {
        if (d.group === 1) {
            labelsGroup1.attr("visibility", "visible");
        } else if (d.group === 2) {
            labelsGroup2.attr("visibility", "visible");
        } else if (d.group === 3) {
            labelsGroup3.attr("visibility", "visible");
        }
    }

}

function mouseLeave(event, d) {
    const originalRadius = (d.id === 1 || d.id === 2 || d.id === 3) ? nodeRadiusCenter : nodeRadius;

    d3.select(this)
      .transition()
      .duration(150)
      .attr("r", originalRadius)  // Return to original radius

    labelsCategories.attr("visibility", "visible");
    labelsGroup1.attr("visibility", "hidden");
    labelsGroup2.attr("visibility", "hidden");
    labelsGroup3.attr("visibility", "hidden");

}

// Set the position attributes of links and nodes each time the simulation ticks.
function ticked() {

    linkPapers
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    linkCategories
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

    labelsCategories
        .attr("transform", d => `translate(${d.x}, ${d.y})`);

    labelsGroup1
        .attr("transform", d => `translate(${d.x}, ${d.y})`);

    labelsGroup2
        .attr("transform", d => `translate(${d.x}, ${d.y})`);

    labelsGroup3
        .attr("transform", d => `translate(${d.x}, ${d.y})`);
        
        simulation.alpha(0.1).restart();
}

function resizeGraph() {
    width = window.innerWidth;
    height = window.innerHeight;

    svg.attr("width", width)
       .attr("height", height);

    simulation.force("center", d3.forceCenter(width / 2, height / 2))
              .alpha(0.2).restart(); // Restart the simulation for the new size
}

// Add resize event listener
window.addEventListener('resize', resizeGraph);

document.getElementById("clinical").addEventListener("mouseover", function() {
    const node = d3.selectAll("circle").filter(d => d.group === 1);
    node.style("fill", "red");

    labelsCategories.attr("visibility", "hidden");
    labelsGroup1.attr("visibility", "visible");

});

document.getElementById("clinical").addEventListener("mouseleave", function() {
    d3.selectAll("circle")
    .filter(d => d.group === 1)
    .style("fill", "blue");

    labelsCategories.attr("visibility", "visible");
    labelsGroup1.attr("visibility", "hidden");
});


document.getElementById("imaging").addEventListener("mouseover", function() {
    const node = d3
    .selectAll("circle")
    .filter(d => d.group === 2);
    node.style("fill", "red");

    labelsCategories.attr("visibility", "hidden");
    labelsGroup2.attr("visibility", "visible");
});

document.getElementById("imaging").addEventListener("mouseleave", function() {
    d3.selectAll("circle")
    .filter(d => d.group === 2)
    .style("fill", "orange");

    labelsCategories.attr("visibility", "visible");
    labelsGroup2.attr("visibility", "hidden");
});

document.getElementById("algorithmic").addEventListener("mouseover", function() {
    const node = d3.selectAll("circle").filter(d => d.group === 3);
    node.style("fill", "red");

    labelsCategories.attr("visibility", "hidden");
    labelsGroup3.attr("visibility", "visible");

});

document.getElementById("algorithmic").addEventListener("mouseleave", function() {
    d3.selectAll("circle")
    .filter(d => d.group === 3)
    .style("fill", "green");

    labelsCategories.attr("visibility", "visible");
    labelsGroup3.attr("visibility", "hidden");
});
