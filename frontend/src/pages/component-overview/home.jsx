import React from 'react';

// material-ui
import {
  Grid,
  Typography,
  Box,
  Stack,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip
} from '@mui/material';

// Mui Icons - replacing Ant Design icons for self-containment
import WorkIcon from '@mui/icons-material/Work';
import PeopleIcon from '@mui/icons-material/People';
import FactCheckIcon from '@mui/icons-material/FactCheck';
import EventIcon from '@mui/icons-material/Event';

// ==============================|| PLACEHOLDER COMPONENTS ||============================== //
// Replicating the look of MainCard based on the provided theme
const MainCard = ({ children, sx = {}, ...other }) => (
  <Card
    sx={{
      borderRadius: 2,
      boxShadow: '0px 2px 8px rgba(0,0,0,0.1)',
      ...sx
    }}
    {...other}
  >
    <CardContent>{children}</CardContent>
  </Card>
);

// Replicating the AnalyticEcommerce card
const AnalyticEcommerce = ({ title, count, percentage, isLoss = false, color = 'primary' }) => (
  <MainCard>
    <Stack spacing={1}>
      <Typography variant="subtitle1" color="text.secondary">
        {title}
      </Typography>
      <Stack direction="row" alignItems="center" spacing={1}>
        <Typography variant="h4">{count}</Typography>
        <Chip label={`${percentage}%`} color={isLoss ? 'warning' : 'success'} size="small" sx={{ fontWeight: 'bold' }} />
      </Stack>
    </Stack>
  </MainCard>
);

// Score Chip for Candidate Table
const ScoreChip = ({ score }) => {
  let color = 'default';
  if (score >= 85) color = 'success';
  else if (score >= 70) color = 'warning';
  else color = 'error';
  return <Chip label={`${score}%`} color={color} variant="outlined" size="small" />;
};

// Placeholder data
const recentCandidatesData = [
  { id: 1, name: 'John Doe', job: 'Senior Frontend Developer', score: 92, date: 'Today, 2:00 PM' },
  { id: 2, name: 'Jane Smith', job: 'UX/UI Designer', score: 88, date: 'Today, 11:30 AM' },
  { id: 3, name: 'Peter Jones', job: 'Senior Frontend Developer', score: 75, date: 'Yesterday, 4:00 PM' },
  { id: 4, name: 'Maria Garcia', job: 'Lead Backend Engineer', score: 95, date: 'Yesterday, 10:00 AM' }
];

const upcomingInterviews = [
  { name: 'Alex Johnson', job: 'UX/UI Designer', time: 'Today, 3:00 PM', avatar: '/static/images/avatar/1.jpg' },
  { name: 'Samantha Williams', job: 'Lead Backend Engineer', time: 'Tomorrow, 10:00 AM', avatar: '/static/images/avatar/2.jpg' }
];

// ==============================|| DASHBOARD - TA HOME PAGE ||============================== //

export default function HomePage() {
  return (
    <Grid container rowSpacing={3} columnSpacing={2.75}>

      {/* row 2 - Stat Cards */}
      <Grid item xs={12} sm={6} lg={3}>
        <AnalyticEcommerce title="Open Positions" count="12" percentage={10.5} />
      </Grid>
      <Grid item xs={12} sm={6} lg={3}>
        <AnalyticEcommerce title="Resumes Processed" count="1,205" percentage={32.8} />
      </Grid>
      <Grid item xs={12} sm={6} lg={3}>
        <AnalyticEcommerce title="Candidates Shortlisted" count="89" percentage={7.4} />
      </Grid>
      <Grid item xs={12} sm={6} lg={3}>
        <AnalyticEcommerce title="Interviews Scheduled" count="42" percentage={15.2} isLoss color="warning" />
      </Grid>

      {/* row 3 - Recent Candidates Table */}
      <Grid item xs={12}>
        <MainCard>
          <Typography variant="h6" gutterBottom>
            Recently Screened Candidates
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Candidate Name</TableCell>
                  <TableCell>Applied For</TableCell>
                  <TableCell align="center">Relevance Score</TableCell>
                  <TableCell>Date Screened</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {recentCandidatesData.map((row) => (
                  <TableRow key={row.id} hover sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                    <TableCell component="th" scope="row">
                      {row.name}
                    </TableCell>
                    <TableCell>{row.job}</TableCell>
                    <TableCell align="center">
                      <ScoreChip score={row.score} />
                    </TableCell>
                    <TableCell>{row.date}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </MainCard>
      </Grid>

      {/* row 4 - Hiring Pipeline & Upcoming Interviews */}
      <Grid item xs={12} md={7}>
        <MainCard>
          <Typography variant="h6" gutterBottom>
            Hiring Pipeline Overview
          </Typography>
          <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'primary.light' }}>
                  <PeopleIcon color="primary" />
                </Avatar>
              </ListItemAvatar>
              <ListItemText primary="Total Applicants" secondary="1,205 Candidates" />
              <Typography variant="h6">100%</Typography>
            </ListItem>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'info.light' }}>
                  <FactCheckIcon color="info" />
                </Avatar>
              </ListItemAvatar>
              <ListItemText primary="Shortlisted" secondary="89 Candidates" />
              <Typography variant="h6">7.4%</Typography>
            </ListItem>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'secondary.light' }}>
                  <EventIcon color="secondary" />
                </Avatar>
              </ListItemAvatar>
              <ListItemText primary="Interview Stage" secondary="42 Candidates" />
              <Typography variant="h6">3.5%</Typography>
            </ListItem>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'success.light' }}>
                  <WorkIcon color="success" />
                </Avatar>
              </ListItemAvatar>
              <ListItemText primary="Offers Extended" secondary="8 Candidates" />
              <Typography variant="h6">0.6%</Typography>
            </ListItem>
          </List>
        </MainCard>
      </Grid>
      <Grid item xs={12} md={5}>
        <MainCard>
          <Typography variant="h6" gutterBottom>
            Upcoming Interviews
          </Typography>
          <List>
            {upcomingInterviews.map((interview, index) => (
              <ListItem key={index} divider>
                <ListItemAvatar>
                  <Avatar alt={interview.name} src={interview.avatar} />
                </ListItemAvatar>
                <ListItemText primary={interview.name} secondary={`${interview.job} - ${interview.time}`} />
              </ListItem>
            ))}
          </List>
        </MainCard>
      </Grid>
    </Grid>
  );
}
