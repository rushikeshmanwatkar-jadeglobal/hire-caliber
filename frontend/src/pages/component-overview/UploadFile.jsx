import React, { useRef, useState } from 'react';
import { Box, Typography, Button, Paper, Stack, IconButton } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import DeleteIcon from '@mui/icons-material/Delete';
import { postRequest } from '../../utils/apiClient';
export default function UploadFile() {
  const [selectedFile, setSelectedFile] = useState(null);
  const inputRef = useRef();
  const maxFileSize = 5 * 1024 * 1024;

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.size > maxFileSize) {
      alert('File size exceeds 5 MB limit.');
      e.target.value = '';
      return;
    }

    setSelectedFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.size > maxFileSize) {
      alert('File size exceeds 5 MB limit.');
      return;
    }
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('resume', selectedFile);

    try {
      const jobId = '1';
      const result = await postRequest(`/jobs/${jobId}/resumes`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      // const result = await response.json();
      alert(`✅ File "${selectedFile.name}" uploaded successfully!`);
      console.log(result);
      setSelectedFile(null);
    } catch (error) {
      alert('❌ Upload failed. Please try again.');
      console.error(error);
    }
  };

  return (
    <Paper
      elevation={3}
      sx={{
        p: 2,
        borderRadius: 3,
        minWidth: ' 100%',
        height: 500,
        maxWidth: ' 100%',
        mx: 'auto',
        mt: 2,
        textAlign: 'center',
        background: 'linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%)'
      }}
    >
      <Typography variant="h5" fontWeight={600} gutterBottom color="primary">
        Upload Your Resume
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Drag & drop your resume file here or click below to browse.
        <br /> Supported formats: <b>.pdf, .doc, .docx</b> | Max size: <b>5 MB</b>
      </Typography>

      <Box
        sx={{
          border: '2px dashed #1976d2',
          borderRadius: 2,
          p: 5,
          backgroundColor: '#fafafa',
          cursor: 'pointer',
          transition: '0.3s',
          '&:hover': { backgroundColor: '#f0f8ff' }
        }}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <CloudUploadIcon sx={{ fontSize: 50, color: '#1976d2' }} />
        <Typography variant="body1" sx={{ mt: 1 }}>
          Drag & Drop or Click to Upload
        </Typography>
        <input type="file" ref={inputRef} accept=".pdf,.doc,.docx" style={{ display: 'none' }} onChange={handleFileChange} />
      </Box>

      {selectedFile && (
        <Stack
          direction="row"
          alignItems="center"
          justifyContent="center"
          spacing={2}
          sx={{
            mt: 3,
            p: 2,
            borderRadius: 2,
            backgroundColor: '#ffffff',
            boxShadow: '0 2px 6px rgba(0,0,0,0.1)'
          }}
        >
          <InsertDriveFileIcon color="primary" />
          <Typography variant="body2" sx={{ fontWeight: 500 }}>
            {selectedFile.name}
          </Typography>
          <IconButton size="small" color="error" onClick={() => setSelectedFile(null)}>
            <DeleteIcon />
          </IconButton>
        </Stack>
      )}

      <Box sx={{ mt: 4 }}>
        <Button
          variant="contained"
          size="large"
          disabled={!selectedFile}
          onClick={handleUpload}
          sx={{
            px: 5,
            py: 1.5,
            borderRadius: 3,
            textTransform: 'none',
            fontWeight: 600
          }}
        >
          Convert and Store
        </Button>
      </Box>
    </Paper>
  );
}
