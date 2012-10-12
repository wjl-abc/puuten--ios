//
//  LibViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import "LibViewController.h"
#import "ImageViewCell.h"
#import "WBViewController.h"
#import "BSHeader.h"

@interface LibViewController ()

@end

@implementation LibViewController
@synthesize categ = _categ;

- (void)setCateg:(NSString *)categ{
    _categ = categ;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    self.view = [[UIView alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    
    //[[UINavigationBar appearance] setTintColor:[UIColor blackColor]];
    
    // Build an array of controllers
    NSMutableArray *controllers = [NSMutableArray array];
    
    
    UIStoryboard *info_board = [UIStoryboard storyboardWithName:@"content" bundle:nil];
    ContentViewController *info = [info_board  instantiateInitialViewController];
    info.categ = _categ;
    info.type = @"4";
    info.title = @"资讯";
    [controllers addObject:info];
    
    UIStoryboard *display_board = [UIStoryboard storyboardWithName:@"content" bundle:nil];
    ContentViewController *display = [display_board  instantiateInitialViewController];
    display.categ = _categ;
    display.type = @"5";
    display.title = @"逛街";
    [controllers addObject:display];
    
    UIStoryboard *feedback_board = [UIStoryboard storyboardWithName:@"content" bundle:nil];
    ContentViewController *feedback = [feedback_board  instantiateInitialViewController];
    feedback.categ = _categ;
    feedback.type = @"6";
    feedback.title = @"点评";
    [controllers addObject:feedback];
    
    tabBarController = [[UITabBarController alloc] init];
    tabBarController.viewControllers = controllers;
    tabBarController.customizableViewControllers = controllers;
    tabBarController.delegate = self;
    
    [self.view addSubview: tabBarController.view];
    self.navigationController.navigationBar.hidden = YES;
	// Do any additional setup after loading the view.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}




@end
