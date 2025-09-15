// // src/pages/Jobs/JobDetails.jsx
// import React, { useState, useEffect, useCallback } from 'react';
// import PropTypes from 'prop-types';
// import {
//   Card,
//   CircularProgress,
//   IconButton,
//   Tooltip,
//   Box,
//   Typography,
//   Alert,
//   Table,
//   TableBody,
//   TableCell,
//   TableContainer,
//   TableHead,
//   TableRow,
//   Paper,
//   Button
// } from '@mui/material';
// // import { Visibility as VisibilityIcon } from '@mui/icons-material'; // Import VisibilityIcon

// // import { getJob, findCandidatesForJob } from '../../utils/apiClient'; // Import API functions

// import { getRequest, postRequest } from '../../utils/apiClient';

// const JobDetails = ({ jobId }) => {
//   const [job, setJob] = useState(null);
//   const [candidates, setCandidates] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [candidatesLoading, setCandidatesLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const fetchJobDetails = useCallback(async () => {
//     setLoading(true);
//     setError(null);
//     try {
//       const data = await getRequest(`/jobs/${jobId}`); // Replace endpoint as per your backend
//       setJob(data);
//     } catch (err) {
//       setError(err.message || 'Could not fetch job details.');
//     } finally {
//       setLoading(false);
//     }
//   }, [jobId]);

//   const handleScreenResumes = async () => {
//     setCandidatesLoading(true);
//     setError(null);
//     try {
//       const data = await postRequest(`/jobs/${jobId}/screen-candidates`, {}); // Replace endpoint and body if needed
//       setCandidates(data);
//     } catch (err) {
//       setError(err.message || 'Could not fetch candidates.');
//     } finally {
//       setCandidatesLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchJobDetails();
//   }, [fetchJobDetails]);

//   if (loading) {
//     return (
//       <Box display="flex" justifyContent="center" alignItems="center" p={3}>
//         <CircularProgress />
//       </Box>
//     );
//   }

//   if (error) {
//     return (
//       <Box p={3}>
//         <Alert severity="error">{error}</Alert>
//       </Box>
//     );
//   }

//   const handleViewResume = (resumeUrl) => {
//     window.open(resumeUrl, '_blank');
//   };

//   return (
//     <Card>
//       <Box p={3}>
//         <Typography variant="h5" gutterBottom>
//           {job.title}
//         </Typography>
//         <Typography variant="subtitle1">Level: {job.level}</Typography>
//         <Typography variant="subtitle1">
//           Experience: {job.experience.min} - {job.experience.max} years
//         </Typography>
//         {/* Display other job details here */}
//         <Button variant="contained" onClick={handleScreenResumes} disabled={candidatesLoading}>
//           {candidatesLoading ? 'Screening...' : 'Screen Resumes'}
//         </Button>
//         {candidates.length > 0 && (
//           <Box mt={3}>
//             <Typography variant="h6" gutterBottom>
//               Eligible Candidates
//             </Typography>
//             <TableContainer component={Paper}>
//               <Table>
//                 <TableHead>
//                   <TableRow>
//                     <TableCell>Name</TableCell>
//                     <TableCell>Skills</TableCell>
//                     <TableCell align="right">Actions</TableCell>
//                   </TableRow>
//                 </TableHead>
//                 <TableBody>
//                   {candidates.map((candidate) => (
//                     <TableRow key={candidate.id}>
//                       <TableCell>{candidate.name}</TableCell>
//                       <TableCell>{candidate.skills.join(', ')}</TableCell>
//                       <TableCell align="right">
//                         <Button variant="outlined" onClick={() => handleViewResume(candidate.resumeUrl)}>
//                           View Resume
//                         </Button>
//                       </TableCell>
//                     </TableRow>
//                   ))}
//                 </TableBody>
//               </Table>
//             </TableContainer>
//           </Box>
//         )}
//       </Box>
//     </Card>
//   );
// };

// JobDetails.propTypes = {
//   jobId: PropTypes.string.isRequired
// };

// export default JobDetails;

// src/pages/Jobs/JobDetails.jsx
import React, { useState, useEffect, useCallback } from 'react';
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
import { Visibility as VisibilityIcon } from '@mui/icons-material'; // Import useParams
import { useParams, useLocation } from 'react-router-dom';
import { getRequest, postRequest } from '../../utils/apiClient'; // Import API functions

const JobDetails = () => {
  const { jobId } = useParams(); // Extract jobId from URL
  const location = useLocation();
  const [job, setJob] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [candidatesLoading, setCandidatesLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchJobDetails = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRequest(`/jobs/${jobId}`); // Replace endpoint as per your backend
      setJob(data);
    } catch (err) {
      setError(err.message || 'Could not fetch job details.');
    } finally {
      setLoading(false);
    }
  }, [jobId]);

  const fetchCandidates = async () => {
    setCandidatesLoading(true);
    setError(null);
    try {
      const data = await postRequest(`/jobs/screen-candidates/${jobId}`, {}); // Replace endpoint and body if needed
      setCandidates(data);
      setCandidates([{ id: '1', name: 'mock user', skills: ['a', 'b'] }]);
    } catch (err) {
      setError(err.message || 'Could not fetch candidates.');
    } finally {
      setCandidatesLoading(false);
    }
  };

  useEffect(() => {
    fetchJobDetails();
  }, [fetchJobDetails]);
  // useEffect(() => {
  // Simulate fetching job details
  //   const fetchDummyJob = async () => {
  //     setLoading(true);
  //     try {
  //       // Simulate API delay
  //       await new Promise((resolve) => setTimeout(resolve, 500));

  //       // Set dummy job data
  //       setJob({
  //         title: 'Frontend Developer',
  //         description: 'get actual description using api call '
  //       });
  //     } catch (err) {
  //       setError('Could not fetch job details.');
  //     } finally {
  //       setLoading(false); // ✅ Important to stop the spinner
  //     }
  //   };

  //   fetchDummyJob();
  // }, []);

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
  const handleFindCandidates = async () => {
    await fetchCandidates();
  };
  const handleViewResume = (resumeUrl) => {
    window.open(resumeUrl, '_blank');
  };

  return (
    <Card>
      <Box p={3}>
        <Typography variant="h3" gutterBottom>
          {job?.title}
        </Typography>
        <Typography variant="h6">{job?.description}</Typography>
        {/* Display other job details here */}
        <Box my={5}>
          <Button variant="contained" onClick={handleFindCandidates} disabled={candidatesLoading}>
            {candidatesLoading ? 'Screening...' : 'Find Candidates'}
          </Button>
        </Box>
        {candidates.length > 0 && (
          <Card m={2}>
            <Box p={2}>
              <Typography variant="h5" gutterBottom>
                Potential Candidates
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Skills</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {candidates.map((candidate) => (
                      <TableRow key={candidate.id}>
                        <TableCell>{candidate.name}</TableCell>
                        <TableCell>{candidate.skills.join(', ')}</TableCell>
                        <TableCell align="right">
                          <Button variant="outlined" onClick={() => handleViewResume(candidate.resumeUrl)}>
                            View Resume
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          </Card>
        )}
      </Box>
    </Card>
  );
};

export default JobDetails;
