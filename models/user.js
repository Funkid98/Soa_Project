const mongoose = require('mongoose');
const { customAlphabet } = require('nanoid');

const generateNumEtud = () => {
    const year = new Date().getFullYear().toString().slice(-2); 
    const random = customAlphabet('0123456789', 4)(); 
    return `${year}-${random}`;
};

const userSchema = new mongoose.Schema({
    name: { type: String, required: true },
    lastname: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    role: { 
        type: String, 
        enum: ['Admin', 'Enseignant', 'Etudiant'],
        default: 'Etudiant',
        required: true 
    },
    birth_date: { type: Date },
    num_etud: { 
        type: String,
        unique: true,
        sparse: true,
        required: function() { return this.role === 'Etudiant'; },
        default: function() { return this.role === 'Etudiant' ? generateNumEtud() : undefined; }
    },
    year_of_stud: {
        type: String,
        required: function() { return this.role === 'Etudiant'; },
        default: function() {
            const year = new Date().getFullYear();
            return `${year}-${year + 1}`;
        }
    },
    field: { type: String, required: function() { return this.role === 'Etudiant'; } },
    department: { type: String, required: function() { return this.role === 'Enseignant'; } },
    specialization: { type: String, required: function() { return this.role === 'Enseignant'; } }
}, { timestamps: true });

module.exports = mongoose.model('User', userSchema);
