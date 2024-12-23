const express = require('express');
const router = express.Router();
const Incident = require('../model/incident');
const mongoose=require("mongoose");
router.get('/', async (req, res) => {
  try {
     const {
       page = 1,
       limit = 10,
       sector,
       threat_level,
       incident_type
     } = req.query;

     const query = {};
     if (sector) query.Sector = sector;
     if (threat_level) query.Threat_Level = threat_level;
     if (incident_type) query.Incident_Type = incident_type;

     const pageNumber = parseInt(page);
     const limitNumber = parseInt(limit);

     const totalDocuments = await Incident.countDocuments(query);
     
     const incidents = await Incident.find(query)
       .sort({ Date: -1 })
       .limit(limitNumber)
       .skip((pageNumber - 1) * limitNumber);

     res.json({
       incidents,
       totalPages: Math.ceil(totalDocuments / limitNumber),
       currentPage: pageNumber,
       totalDocuments
     });
  } catch (error) {
    console.error('Error fetching incidents:', error);
    res.status(500).json({
      message: 'Error fetching incidents',
      error: error.message
    });
  }
});


router.get('/:id', async (req, res) => {
  const { id } = req.params;

  if (!mongoose.Types.ObjectId.isValid(id)) {
    return res.status(400).json({ message: 'Invalid ID format' });
  }

  try {
    const incident = await Incident.findById(id);

    if (!incident) {
      return res.status(404).json({ message: 'Incident not found' });
    }

    res.json(incident);
  } catch (error) {
    console.error('Error fetching incident:', error);
    res.status(500).json({ 
      message: 'Error fetching incident', 
      error: error.message 
    });
  }
});

module.exports = router;


router.post('/', async (req, res) => {
  try {
    
    const newIncident = new Incident(req.body);
    const savedIncident = await newIncident.save();
    
    res.status(201).json(savedIncident);
  } catch (error) {
    console.error('Error creating incident:', error);
    res.status(400).json({ 
      message: 'Error creating incident', 
      error: error.message 
    });
  }
});


router.patch('/:id', async (req, res) => {
  try {
    const updatedIncident = await Incident.findByIdAndUpdate(
      req.params.id, 
      req.body, 
      { 
        new: true,  
        runValidators: true 
      }
    );
    
    if (!updatedIncident) {
      return res.status(404).json({ message: 'Incident not found' });
    }
    
    res.json(updatedIncident);
  } catch (error) {
    console.error('Error updating incident:', error);
    res.status(400).json({ 
      message: 'Error updating incident', 
      error: error.message 
    });
  }
});
  

router.get('/stats/overview', async (req, res) => {
  try {
    const totalIncidents = await Incident.countDocuments();
    const criticalIncidents = await Incident.countDocuments({ Threat_Level: 'Critical' });
    const unsolvedIncidents = await Incident.countDocuments({ Incident_Solved: false });

    const sectorBreakdown = await Incident.aggregate([
      { 
        $group: { 
          _id: '$Sector', 
          count: { $sum: 1 } 
        }
      },
      { 
        $sort: { count: -1 } 
      }
    ]);

    res.json({
      totalIncidents,
      criticalIncidents,
      unsolvedIncidents,
      sectorBreakdown
    });
  } catch (error) {
    console.error('Error fetching stats:', error);
    res.status(500).json({ 
      message: 'Error fetching statistics', 
      error: error.message 
    });
  }
});

module.exports = router;