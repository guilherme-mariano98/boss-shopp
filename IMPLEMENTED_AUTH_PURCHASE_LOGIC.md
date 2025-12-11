# Implemented Authentication Logic for Purchases

## Overview
This document describes the changes made to implement the requirement that users can only make purchases when they are logged in.

## Changes Made

### 1. Purchase Page Authentication Check
**File:** `src/frontend/purchase.js`
- Added authentication verification at the beginning of `initPurchasePage()` function
- If user is not authenticated, they are redirected to the login page with an appropriate message

### 2. Add to Cart Authentication Check
**File:** `src/frontend/script.js`
- Modified `addToCart()` function to verify user authentication before adding items to cart
- If user is not authenticated, a login modal is displayed with a warning message

### 3. Checkout Authentication Check
**File:** `src/frontend/script.js`
- Modified `checkout()` function to verify user authentication before proceeding
- If user is not authenticated, a login modal is displayed with a warning message

### 4. Enhanced Notification System
**File:** `src/frontend/purchase.js`
- Updated `showNotification()` function to support different notification types (success, warning, error, info)
- Added appropriate color coding for different notification types

### 5. Improved Login Modal Message
**File:** `src/frontend/script.js`
- Updated the login modal message to be more descriptive about why login is needed

## How It Works

1. **Authentication Verification:** The system checks for the presence of `authToken` and `user` in localStorage
2. **Access Control:** 
   - Unauthenticated users attempting to access the purchase page are redirected to login
   - Unauthenticated users trying to add items to cart see a login prompt
   - Unauthenticated users trying to checkout see a login prompt
3. **User Experience:** Clear notifications inform users why they need to log in

## Technical Details

The authentication check uses the following logic:
```javascript
const authToken = localStorage.getItem('authToken');
const user = localStorage.getItem('user');

if (!authToken || !user) {
    // User is not authenticated
    // Show login modal or redirect to login page
}
```

This approach ensures that all purchase-related actions require authentication while providing clear feedback to users about why authentication is needed.