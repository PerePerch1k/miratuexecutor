local hub = Instance.new("ScreenGui")
hub.Name = "Miratu HUB"
hub.Parent = game.Players.LocalPlayer.PlayerGui

local mainFrame = Instance.new("Frame")
mainFrame.Size = UDim2.new(0, 600, 0, 500)
mainFrame.Position = UDim2.new(0.5, -300, 0.5, -250)
mainFrame.BackgroundColor3 = Color3.new(0, 0, 0)
mainFrame.BackgroundTransparency = 0.5
mainFrame.Parent = hub

local titleLabel = Instance.new("TextLabel")
titleLabel.Text = "Miratu HUB"
titleLabel.Font = Enum.Font.SourceSans
titleLabel.FontSize = Enum.FontSize.Size24
titleLabel.TextColor3 = Color3.new(1, 1, 1)
titleLabel.Parent = mainFrame

local buttonFrame = Instance.new("Frame")
buttonFrame.Size = UDim2.new(0, 580, 0, 450)
buttonFrame.Position = UDim2.new(0, 10, 0, 40)
buttonFrame.BackgroundColor3 = Color3.new(0, 0, 0)
buttonFrame.BackgroundTransparency = 0.5
buttonFrame.Parent = mainFrame

local buttonTemplate = Instance.new("TextButton")
buttonTemplate.Size = UDim2.new(0, 560, 0, 30)
buttonTemplate.Font = Enum.Font.SourceSans
buttonTemplate.FontSize = Enum.FontSize.Size18
buttonTemplate.TextColor3 = Color3.new(1, 1, 1)
buttonTemplate.BackgroundColor3 = Color3.new(0, 0, 0)
buttonTemplate.BackgroundTransparency = 0.5

local killButton = buttonTemplate:Clone()
killButton.Text = "Kill"
killButton.Parent = buttonFrame
killButton.Position = UDim2.new(0, 10, 0, 10)
killButton.MouseButton1Click:Connect(function()
    game.Players.LocalPlayer.Character.Humanoid.Health = 0
end)

local walkspeedButton = buttonTemplate:Clone()
walkspeedButton.Text = "Walkspeed 100"
walkspeedButton.Parent = buttonFrame
walkspeedButton.Position = UDim2.new(0, 10, 0, 50)
walkspeedButton.MouseButton1Click:Connect(function()
    game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = 100
end)

local jumppowerButton = buttonTemplate:Clone()
jumppowerButton.Text = "Jumppower 200"
jumppowerButton.Parent = buttonFrame
jumppowerButton.Position = UDim2.new(0, 10, 0, 90)
jumppowerButton.MouseButton1Click:Connect(function()
    game.Players.LocalPlayer.Character.Humanoid.JumpPower = 200
end)

local bangButton = buttonTemplate:Clone()
bangButton.Text = "Bang"
bangButton.Parent = buttonFrame
bangButton.Position = UDim2.new(0, 10, 0, 130)
bangButton.MouseButton1Click:Connect(function()
    local speaker = game.Players.LocalPlayer
    local humanoid = speaker.Character:FindFirstChildWhichIsA("Humanoid")
    bangAnim = Instance.new("Animation")
    bangAnim.AnimationId = not r15(speaker) and "rbxassetid://148840371" or "rbxassetid://5918726674"
    bang = humanoid:LoadAnimation(bangAnim)
    bang:Play()
end)

local clearWeaponsButton = buttonTemplate:Clone()
clearWeaponsButton.Text = "Clear all weapons"
clearWeaponsButton.Parent = buttonFrame
clearWeaponsButton.Position = UDim2.new(0, 10, 0, 170)
clearWeaponsButton.MouseButton1Click:Connect(function()
    local character = game.Players.LocalPlayer.Character
    for _, child in ipairs(character:GetChildren()) do
        if child:IsA("Tool") then
            child:Destroy()
        end
    end
end)

local freezeButton = buttonTemplate:Clone()
freezeButton.Text = "Freeze"
freezeButton.Parent = buttonFrame
freezeButton.Position = UDim2.new(0, 10, 0, 210)
freezeButton.MouseButton1Click:Connect(function()
    local character = game.Players.LocalPlayer.Character
    local humanoid = character:FindFirstChildWhichIsA("Humanoid")
    local rootPart = character:FindFirstChild("HumanoidRootPart")
    local rootPartPos = rootPart.Position
    humanoid.PlatformStand = true
    while wait(0.1) do
        humanoid.PlatformStand = true
        rootPart.Position = rootPartPos
    end
end)

local teleportButton = buttonTemplate:Clone()
teleportButton.Text = "Teleport"
teleportButton.Parent = buttonFrame
teleportButton.Position = UDim2.new(0, 10, 0, 250)
teleportButton.MouseButton1Click:Connect(function()
    local character = game.Players.LocalPlayer.Character
    local humanoid = character:FindFirstChildWhichIsA("Humanoid")
    local rootPart = character:FindFirstChild("HumanoidRootPart")
    local playerGui = game.Players.LocalPlayer:FindFirstChild("PlayerGui")
    local textBox = Instance.new("TextBox")
    textBox.Size = UDim2.new(0, 300, 0, 20)
    textBox.Font = Enum.Font.SourceSans
    textBox.FontSize = Enum.FontSize.Size18
    textBox.Text = "Enter position (X, Y, Z)"
    textBox.Parent = playerGui
    local okButton = Instance.new("TextButton")
    okButton.Size = UDim2.new(0, 50, 0, 20)
    okButton.Font = Enum.Font.SourceSans
    okButton.FontSize = Enum.FontSize.Size18
    okButton.Text = "OK"
    okButton.TextColor3 = Color3.new(1, 1, 1)
    okButton.BackgroundColor3 = Color3.new(0, 0, 0)
    okButton.BackgroundTransparency = 0.5
    okButton.Parent = playerGui
    okButton.Position = UDim2.new(0, 310, 0, 20)
    okButton.MouseButton1Click:Connect(function()
        local coords = {}
        for coord in textBox.Text:gmatch("[%-%d%.]+") do
            table.insert(coords, tonumber(coord))
        end
        if #coords == 3 then
            rootPart.Position = Vector3.new(coords[1], coords[2], coords[3])
        end
        textBox:Destroy()
        okButton:Destroy()
    end)
end)

local godButton = buttonTemplate:Clone()
godButton.Text = "GOD mode"
godButton.Parent = buttonFrame
godButton.Position = UDim2.new(0, 10, 0, 290)
godButton.MouseButton1Click:Connect(function()
    local character = game.Players.LocalPlayer.Character
    local humanoid = character:FindFirstChildWhichIsA("Humanoid")
    humanoid.MaxHealth = math.huge
    humanoid.Health = math.huge
end)

local unbangButton = buttonTemplate:Clone()
unbangButton.Text = "Unbang"
unbangButton.Parent = buttonFrame
unbangButton.Position = UDim2.new(0, 10, 0, 330)
unbangButton.MouseButton1Click:Connect(function()
    if bangDied then
        bangDied:Disconnect()
        bang:Stop()
        bangAnim:Destroy()
        bangLoop:Disconnect()
    end
end)

local swimButton = buttonTemplate:Clone()
swimButton.Text = "Swim"
swimButton.Parent = buttonFrame
swimButton.Position = UDim2.new(0, 10, 0, 370)
swimButton.MouseButton1Click:Connect(function()
    local speaker = game.Players.LocalPlayer
    local character = speaker.Character
    local humanoid = character:FindFirstChildWhichIsA("Humanoid")
    local swimming = false
    local oldgrav = workspace.Gravity
    local gravReset = nil
    local swimDied = function()
        workspace.Gravity = oldgrav
        swimming = false
    end
    local enums = Enum.HumanoidStateType:GetEnumItems()
    table.remove(enums, table.find(enums, Enum.HumanoidStateType.None))
    for i, v in pairs(enums) do
        humanoid:SetStateEnabled(v, false)
    end
    humanoid:ChangeState(Enum.HumanoidStateType.Swimming)
    local swimbeat = RunService.Heartbeat:Connect(function()
        pcall(function()
            speaker.Character.HumanoidRootPart.Velocity = ((humanoid.MoveDirection ~= Vector3.new() or UserInputService:IsKeyDown(Enum.KeyCode.Space)) and speaker.Character.HumanoidRootPart.Velocity or Vector3.new())
        end)
    end)
    swimming = true
end)

local unswimButton = buttonTemplate:Clone()
unswimButton.Text = "Unswim"
unswimButton.Parent = buttonFrame
unswimButton.Position = UDim2.new(0, 10, 0, 410)

local closeButton = Instance.new("TextButton")
closeButton.Size = UDim2.new(0, 30, 0, 30)
closeButton.Position = UDim2.new(1, -40, 0, 10)
closeButton.Text = "X"
closeButton.Font = Enum.Font.SourceSans
closeButton.FontSize = Enum.FontSize.Size18
closeButton.TextColor3 = Color3.new(1, 1, 1)
closeButton.BackgroundColor3 = Color3.new(1, 0, 0)
closeButton.Parent = mainFrame
closeButton.MouseButton1Click:Connect(function()
    mainFrame:Destroy()
end)

local dragging = false
local dragInput
local dragStart
local startPos

mainFrame.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = true
        dragStart = input.Position
        startPos = mainFrame.Position

        input.Changed:Connect(function()
            if input.UserInputState == Enum.UserInputState.End then
                dragging = false
            end
        end)
    end
end)

mainFrame.InputChanged:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseMovement then
        dragInput = input
    end
end)

game:GetService("UserInputService").InputChanged:Connect(function(input)
    if input == dragInput and dragging then
        local delta = input.Position - dragStart
        mainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end
end)
