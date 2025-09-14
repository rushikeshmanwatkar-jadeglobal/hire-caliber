import React, { useState } from "react";
import { Modal, Card, Grid, Stack, TextField, Typography, MenuItem, Button, Chip, Box, FormControl, InputLabel, Select, TextareaAutosize } from "@mui/material";
import { postRequest } from "../../utils/apiClient";

const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "90%",
  maxWidth: 700,
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
  borderRadius: 2,
};

const JobModal = ({ open, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    title: "",
    description: ""
  });
  const [newSkill, setNewSkill] = useState("");
  const [skillType, setSkillType] = useState("Nice-to-Have");

  const handleFieldChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAddSkill = () => {
    if (newSkill.trim()) {
      setFormData({
        ...formData,
        skills: [...formData.skills, { name: newSkill.trim(), type: skillType }],
      });
      setNewSkill("");
      setSkillType("Nice-to-Have");
    }
  };

  const handleDeleteSkill = (index) => {
    const newSkills = [...formData.skills];
    newSkills.splice(index, 1);
    setFormData({ ...formData, skills: newSkills });
  };

  // New: handle API call on save
  const handleSave = async () => {
    try {
      const res = await postRequest("/jobs/create", formData); // replace endpoint with your API
      if (res) {
        onSave(res); // optionally update parent state
        onClose();
      }
    } catch (error) {
      console.error(error);
      alert("Something went wrong, could not connect to the server!");
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Card sx={modalStyle}>
        <Typography variant="h5" fontWeight="medium" mb={3}>
          Create New Job
        </Typography>

        <Grid container spacing={3} direction="column" my={3}>
          <Grid item xs={12}>
            <Stack direction="column" spacing={2}>
              <TextField
                label="Job Title"
                fullWidth
                name="title"
                value={formData.title}
                onChange={handleFieldChange}
                variant="outlined"
              />
              <TextField
                label="Job Description"
                fullWidth
                name="description"
                value={formData.description}
                onChange={handleFieldChange}
                multiline
                minRows={5}
                maxRows={12}
                variant="outlined"
              />
            </Stack>
          </Grid>
          </Grid>
          <Grid item xs={12}>
            <Stack direction="row" justifyContent="flex-end" spacing={2}>
              <Button variant="outlined" onClick={onClose}>
                Cancel
              </Button>
              <Button variant="contained" onClick={handleSave}>
                Save Job
              </Button>
            </Stack>
          </Grid>
      </Card>
    </Modal>
  );
};

export default JobModal;
