// src/pages/Jobs/JobsList.jsx
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import {
  Card,
  CircularProgress,
  IconButton,
  Tooltip,
  Box,
  Typography,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button
} from '@mui/material';
import { Edit as EditIcon, Add as AddIcon, Visibility as VisibilityIcon } from '@mui/icons-material'; // Import VisibilityIcon
import { Link } from 'react-router-dom';

import JobModal from 'components/Modals/JobModal';

// ✅ New mock data
const mockJobs = [
  {
    id: '1',
    title: 'Servicenow Developer',
    description: `In order to be successful in this role, we need someone who has:
● BS in Computer Science/Engineering or equivalent domain with 5-15 years of cloud applications experience.
● Experience working with wide variety of automated testing tools including Selenium, Programming Language – Java , Unit Test Framework – MSTest / NUnit and TestNG / Junit and other open source tools.
● Setting up automated test framework’s with different tools/ enhancing existing framework.
● Exposure on creating build pipelines using Jenkins.
● Experience working with SCM tools like Git/ SVN.
● Experience in Rest API automation tools like – Rest Assured/ Http Client.
● Knowledge of continuous integration and deployment tools (e.g. Jenkins).
● Experience working in Agile Practices (SAFE, Scrum)`
  },
  {
    id: '2',
    title: 'Oracle HCM techno functional',
    description: `Functional knowledge of Compensation and Equity area in Oracle is plus
-HCM Techno-Functional Engineers / Integration Engineers with core expertise in HCM extract , HCM API integration , HDL imports . Added expertise in Mulesoft would be a highly desirable but not mandatory.
● Oracle HCM Tech (Integrations, Data Conversion , Reports, Fast Formulas, OIC(Optional)) + Functional Coverage.
● Hands-on expertise with Oracle HCM tools such as OTBI, BI Publisher, and HDL/SDL.
● Optional experience with Oracle Integration Cloud (OIC) is a strong advantage.
● Strong problem-solving skills with the ability to work independently and collaboratively in a team.
● Excellent communication and documentation skills.`
  }
];

function ActionsCell({ row }) {
  return (
    <>
      <Tooltip title="View Job">
        <IconButton size="small" sx={{ color: 'grey.400' }} component={Link} to={`/jobs/${row.id}`}>
          <VisibilityIcon fontSize="small" />
        </IconButton>
      </Tooltip>
      <Tooltip title="Edit Job">
        <IconButton size="small" sx={{ color: 'grey.400' }}>
          <EditIcon fontSize="small" />
        </IconButton>
      </Tooltip>
    </>
  );
}

ActionsCell.propTypes = {
  row: PropTypes.object.isRequired
};

const JobsList = () => {
  const [jobs, setJobs] = useState(mockJobs);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [jobToEdit, setJobToEdit] = useState(null);

  const handleOpenCreateModal = () => {
    setJobToEdit(null);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setJobToEdit(null);
  };

  const handleSuccess = () => {
    // Here you can update the list later when connected to API
  };

  const renderContent = () => {
    if (loading) {
      return (
        <Box display="flex" justifyContent="center" alignItems="center" p={3}>
          <CircularProgress />
        </Box>
      );
    }

    if (error) {
      return (
        <Box p={3}>
          <Alert severity="error">{error}</Alert>
        </Box>
      );
    }

    return (
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {jobs.map((job) => (
              <TableRow key={job.id}>
                <TableCell>{job.title}</TableCell>
                <TableCell>{job.description}</TableCell>
                <TableCell align="right">
                  <ActionsCell row={job} />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Box sx={{ p: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleOpenCreateModal}>
            Create Job
          </Button>
        </Box>
      </TableContainer>
    );
  };

  return (
    <Box pt={3} pb={3}>
      <Card>{renderContent()}</Card>
      <JobModal open={modalOpen} onClose={handleCloseModal} onSuccess={handleSuccess} jobToEdit={jobToEdit} />
    </Box>
  );
};

export default JobsList;