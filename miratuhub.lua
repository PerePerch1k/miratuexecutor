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
buttonFrame.Size = UDim2.new(0, 580, 0, 420)
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
killButton.Text = "Suicide"
killButton.Parent = buttonFrame
killButton.Position = UDim2.new(0, 10, 0, 10)
killButton.MouseButton1Click:Connect(function()
    game.Players.LocalPlayer.Character.Humanoid.Health = 0
end)

local walkspeedButton = buttonTemplate:Clone()
walkspeedButton.Text = "Super Speed"
walkspeedButton.Parent = buttonFrame
walkspeedButton.Position = UDim2.new(0, 10, 0, 50)
walkspeedButton.MouseButton1Click:Connect(function()
    game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = 100
end)

local jumppowerButton = buttonTemplate:Clone()
jumppowerButton.Text = "Super Jump"
jumppowerButton.Parent = buttonFrame
jumppowerButton.Position = UDim2.new(0, 10, 0, 90)
jumppowerButton.MouseButton1Click:Connect(function()
    game.Players.LocalPlayer.Character.Humanoid.JumpPower = 200
end)

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
