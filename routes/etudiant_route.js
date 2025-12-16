const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const User = require('../models/user');
const { verifyToken, checkRole } = require('../authmiddlware/middleware');
const router = express.Router();
const JWT_SECRET = process.env.JWT_SECRET;

// -------- REGISTER --------
router.post('/register', [
    body('name').trim().notEmpty().withMessage('Name is required'),
    body('lastname').trim().notEmpty().withMessage('Last name is required'),
    body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
    body('role').isIn(['Admin', 'Enseignant', 'Etudiant']).withMessage('Invalid role')
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { name, lastname, email, password, role, birth_date, num_etud, year_of_stud, field, department, specialization } = req.body;
        
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ message: "Email already in use!" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const userData = { name, lastname, email, password: hashedPassword, role };
        
        if (role === 'Etudiant') {
            Object.assign(userData, { birth_date, num_etud, year_of_stud, field });
        }
        if (role === 'Enseignant') {
            Object.assign(userData, { department, specialization });
        }

        const user = new User(userData);
        await user.save();

        const token = jwt.sign(
            { userId: user._id, email: user.email, role: user.role },
            JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.status(201).json({
            message: "User registered successfully",
            token,
            user: {
                id: user._id,
                name: user.name,
                lastname: user.lastname,
                email: user.email,
                role: user.role
            }
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Server error" });
    }
});

// -------- LOGIN --------
router.post('/login', [
    body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
    body('password').notEmpty().withMessage('Password is required')
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(401).json({ message: "Invalid credentials" });
        }

        const isValidPassword = await bcrypt.compare(password, user.password);
        if (!isValidPassword) {
            return res.status(401).json({ message: "Invalid credentials" });
        }

        const token = jwt.sign(
            { userId: user._id, email: user.email, role: user.role },
            JWT_SECRET,
            { expiresIn: '7d' }
        );

        res.json({
            message: "Login successful",
            token,
            user: {
                id: user._id,
                name: user.name,
                lastname: user.lastname,
                email: user.email,
                role: user.role
            }
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Server error" });
    }
});

// -------- VERIFY TOKEN --------
router.post('/verify-token', (req, res) => {
    const token = req.body.token || req.header('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
        return res.status(400).json({ message: 'No token provided' });
    }
    
    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        res.json({
            valid: true,
            user: decoded
        });
    } catch (err) {
        res.status(401).json({
            valid: false,
            message: 'Invalid or expired token'
        });
    }
});

// -------- GET PROFILE --------
router.get('/profile', verifyToken, async (req, res) => {
    try {
        const user = await User.findById(req.user.userId).select('-password');
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.json(user);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Server error' });
    }
});

// -------- UPDATE USER --------
router.put('/users/:num_etud', verifyToken, async (req, res) => {
    try {
        const user = await User.findOne({ num_etud: req.params.num_etud });
        if (!user) return res.status(404).json({ message: 'User not found' });

        if (req.user.userId !== user._id.toString() && req.user.role !== 'Admin') {
            return res.status(403).json({ message: 'Access forbidden' });
        }

        const { name, lastname, email, birth_date, year_of_stud, field, department, specialization } = req.body;
        const updateData = { name, lastname, email };

        if (user.role === 'Etudiant') {
            if (birth_date) updateData.birth_date = birth_date;
            if (year_of_stud) updateData.year_of_stud = year_of_stud;
            if (field) updateData.field = field;
        }
        if (user.role === 'Enseignant') {
            if (department) updateData.department = department;
            if (specialization) updateData.specialization = specialization;
        }

        const updatedUser = await User.findOneAndUpdate(
            { num_etud: req.params.num_etud },
            updateData,
            { new: true }
        ).select('-password');

        res.json({ message: 'User updated successfully', user: updatedUser });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Server error' });
    }
});

// -------- DELETE USER (Admin only) --------
router.delete('/users/:num_etud', verifyToken, checkRole('Admin'), async (req, res) => {
    try {
        const user = await User.findOneAndDelete(req.params.num_etud);
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.json({ message: 'User deleted successfully' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Server error' });
    }
});

// -------- GET ALL USERS (Admin only) --------
router.get('/users', verifyToken, checkRole('Admin'), async (req, res) => {
    try {
        const users = await User.find().select('-password');
        res.json(users);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Server error' });
    }
});

// -------- GET USERS BY ROLE (Admin and Enseignant) --------
router.get('/users/role/:role', verifyToken, checkRole('Admin', 'Enseignant'), async (req, res) => {
    try {
        const { role } = req.params;
        if (!['Admin', 'Enseignant', 'Etudiant'].includes(role)) {
            return res.status(400).json({ message: 'Invalid role' });
        }

        const users = await User.find({ role }).select('-password');
        res.json(users);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Server error' });
    }
});

module.exports = router;